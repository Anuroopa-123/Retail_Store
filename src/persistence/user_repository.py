# src/persistence/user_repository.py
from __future__ import annotations

from typing import Optional, List, TypedDict
from datetime import datetime, timezone
from sqlalchemy import select, delete, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user import User
from src.domain.entities.auth.role import Role
from src.domain.entities.auth.password_reset_token import PasswordResetToken
from src.domain.entities.auth.email_verification_token import EmailVerificationToken
from src.domain.entities.auth.personal_access_token import PersonalAccessToken
from src.infrastructure.auth.security import hash_password, verify_password
from src.application.models.auth.user_crud_model import (
    UserCreateModel,
    UserUpdateModel,
    UserPasswordUpdateModel,
    UserStatusUpdateModel,
)
from src.application.models.auth.role_model import (
    AssignRolesModel,
    AssignRoleBySlugModel,
)
from src.application.exception_handler import (
    UserNotFoundError,
    DuplicateEmailError,
    InvalidPasswordError,
    RoleNotFoundError,
    TokenInvalidError,
    TokenExpiredError,
)


class PaginatedUsers(TypedDict):
    data: List[User]
    total: int
    limit: int
    offset: int


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # ── helpers ───────────────────────────────────────────────────────────────

    async def _get_user_with_roles(self, field, value) -> Optional[User]:
        """Fetch a user with roles eagerly loaded."""
        result = await self.session.execute(
            select(User)
            .where(field == value)
            .options(selectinload(User.roles))
        )
        return result.scalar_one_or_none()

    async def _get_user_lean(self, field, value) -> Optional[User]:
        """Fetch a user WITHOUT roles — use for auth paths that only need credentials."""
        result = await self.session.execute(
            select(User).where(field == value)
        )
        return result.scalar_one_or_none()

    async def _check_duplicate_email(
        self, email: str, exclude_user_id: Optional[int] = None
    ) -> None:
        query = select(User).where(User.email == email)
        if exclude_user_id:
            query = query.where(User.id != exclude_user_id)
        existing = await self.session.scalar(query)
        if existing:
            raise DuplicateEmailError()

    @staticmethod
    def _ensure_aware(dt: datetime) -> datetime:
        """Return a timezone-aware datetime; assume UTC if naive."""
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt

    # ── fetch ─────────────────────────────────────────────────────────────────

    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await self._get_user_with_roles(User.id, user_id)

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self._get_user_with_roles(User.email, email)

    async def get_authenticate_by_email(self, email: str) -> Optional[User]:
        """Used for login — active users only, roles eager-loaded for permission checks."""
        result = await self.session.execute(
            select(User)
            .where(User.email == email)
            .where(User.status == "active")
            .options(selectinload(User.roles))
        )
        return result.scalar_one_or_none()

    async def get_all_by_tenant(
        self,
        tenant_id: int,
        store_id: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> PaginatedUsers:
        query = (
            select(User)
            .where(User.tenant_id == tenant_id)
            .options(selectinload(User.roles))
        )
        if store_id:
            query = query.where(User.store_id == store_id)

        total = await self.session.scalar(
            select(func.count()).select_from(query.subquery())
        )
        result = await self.session.execute(
            query.limit(limit).offset(offset)
        )
        return PaginatedUsers(
            data=result.scalars().all(),
            total=total,
            limit=limit,
            offset=offset,
        )

    # ── create ────────────────────────────────────────────────────────────────

    async def create(self, data: UserCreateModel) -> User:
        await self._check_duplicate_email(data.email)

        user = User(
            tenant_id=data.tenant_id,
            store_id=data.store_id,
            email=data.email,
            name=data.name,
            password_hash=hash_password(data.password),
            phone=data.phone,
        )
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user, ["roles"])
        return user

    # ── update ────────────────────────────────────────────────────────────────

    async def update(self, user_id: int, data: UserUpdateModel) -> User:
        """
        The service layer guarantees the user exists before calling this method.
        The guard here is a safety net for direct repository usage.
        """
        user = await self.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()

        if data.email and data.email != user.email:
            await self._check_duplicate_email(data.email, exclude_user_id=user_id)
            user.email = data.email
        if data.name:
            user.name = data.name
        if data.phone:
            user.phone = data.phone

        self.session.add(user)
        await self.session.flush()
        return user

    async def update_password(
        self, user_id: int, data: UserPasswordUpdateModel
    ) -> User:
        user = await self.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        if not verify_password(data.current_password, user.password_hash):
            raise InvalidPasswordError()

        user.password_hash = hash_password(data.new_password)
        self.session.add(user)
        await self.session.flush()
        return user

    async def update_status(
        self, user_id: int, data: UserStatusUpdateModel
    ) -> User:
        user = await self.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        user.status = data.status
        self.session.add(user)
        await self.session.flush()
        return user

    # ── roles ─────────────────────────────────────────────────────────────────

    async def assign_roles(self, user_id: int, data: AssignRolesModel) -> User:
        """
        Replace all user roles with the given role IDs.
        Raises RoleNotFoundError if any ID does not exist.
        """
        user = await self.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()

        roles = (await self.session.execute(
            select(Role).where(Role.id.in_(data.role_ids))
        )).scalars().all()

        # Guard: ensure every requested role_id was actually found.
        if len(roles) != len(data.role_ids):
            found_ids = {r.id for r in roles}
            missing = [rid for rid in data.role_ids if rid not in found_ids]
            raise RoleNotFoundError(f"role IDs not found: {missing}")

        user.roles.clear()
        user.roles.extend(roles)
        self.session.add(user)
        await self.session.flush()
        return user

    async def assign_role_by_slug(
        self, user_id: int, data: AssignRoleBySlugModel
    ) -> User:
        """Add a single role by slug without clearing existing roles."""
        user = await self.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()

        role = await self.session.scalar(
            select(Role).where(
                Role.slug == data.role_slug,
                Role.tenant_id == user.tenant_id,
            )
        )
        if not role:
            raise RoleNotFoundError(data.role_slug)

        if role not in user.roles:
            user.roles.append(role)
            self.session.add(user)
            await self.session.flush()

        return user

    async def remove_role(
        self, user_id: int, data: AssignRoleBySlugModel
    ) -> User:
        user = await self.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()

        user.roles = [r for r in user.roles if r.slug != data.role_slug]
        self.session.add(user)
        await self.session.flush()
        return user

    # ── tokens ────────────────────────────────────────────────────────────────

    async def create_password_reset_token(
        self,
        user_id: int,
        token_hash: str,
        expires_at: datetime,
    ) -> PasswordResetToken:
        expires_at = self._ensure_aware(expires_at)

        await self.session.execute(
            delete(PasswordResetToken).where(
                PasswordResetToken.user_id == user_id
            )
        )
        token = PasswordResetToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        self.session.add(token)
        await self.session.flush()
        return token

    async def get_password_reset_token(
        self, token_hash: str
    ) -> Optional[PasswordResetToken]:
        return await self.session.scalar(
            select(PasswordResetToken)
            .where(PasswordResetToken.token_hash == token_hash)
        )

    async def delete_password_reset_token(self, user_id: int) -> None:
        await self.session.execute(
            delete(PasswordResetToken).where(
                PasswordResetToken.user_id == user_id
            )
        )

    async def create_email_verification_token(
        self,
        user_id: int,
        token_hash: str,
        expires_at: datetime,
    ) -> EmailVerificationToken:
        expires_at = self._ensure_aware(expires_at)

        await self.session.execute(
            delete(EmailVerificationToken).where(
                EmailVerificationToken.user_id == user_id
            )
        )
        token = EmailVerificationToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        self.session.add(token)
        await self.session.flush()
        return token

    async def get_email_verification_token(
        self, token_hash: str
    ) -> Optional[EmailVerificationToken]:
        return await self.session.scalar(
            select(EmailVerificationToken)
            .where(EmailVerificationToken.token_hash == token_hash)
        )

    async def verify_email(self, token_hash: str) -> User:
        """
        Persist the email verification. Business-rule validation (expiry,
        replay) is the service layer's responsibility; this method trusts
        the token is valid and just does the writes.
        """
        token = await self.get_email_verification_token(token_hash)
        if not token:
            raise TokenInvalidError()

        now = datetime.now(timezone.utc)
        token.verified_at = now
        self.session.add(token)  # FIX: persist the verified_at timestamp

        user = await self.get_by_id(token.user_id)
        user.email_verified_at = now
        user.status = "active"  # ← Activate user

        self.session.add(user)
        await self.session.flush()
        return user

    async def mark_email_verified(
        self, user_id: int, verified_at: datetime
    ) -> User:
        user = await self.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        user.email_verified_at = self._ensure_aware(verified_at)
        self.session.add(user)
        await self.session.flush()
        return user

    async def create_personal_access_token(
        self,
        user_id: int,
        name: str,
        token_hash: str,
        abilities: list,
        expires_at: Optional[datetime] = None,
    ) -> PersonalAccessToken:
        if expires_at is not None:
            expires_at = self._ensure_aware(expires_at)

        token = PersonalAccessToken(
            user_id=user_id,
            name=name,
            token_hash=token_hash,
            abilities=abilities,
            expires_at=expires_at,
        )
        self.session.add(token)
        await self.session.flush()
        return token

    async def get_personal_access_tokens(
        self, user_id: int
    ) -> List[PersonalAccessToken]:
        result = await self.session.execute(
            select(PersonalAccessToken)
            .where(PersonalAccessToken.user_id == user_id)
        )
        return result.scalars().all()

    async def delete_personal_access_token(
        self, user_id: int, token_id: int
    ) -> bool:
        result = await self.session.execute(
            delete(PersonalAccessToken).where(
                PersonalAccessToken.user_id == user_id,
                PersonalAccessToken.id == token_id,
            )
        )
        return result.rowcount > 0

    # ── delete ────────────────────────────────────────────────────────────────

    async def soft_delete(self, user_id: int) -> bool:
        """
        Internal use only. Prefer UserService.soft_delete which routes
        through update_status for consistent validation.
        """
        user = await self.get_by_id(user_id)
        if not user:
            return False
        user.status = "inactive"
        self.session.add(user)
        await self.session.flush()
        return True

    async def force_delete(self, user_id: int) -> bool:
        result = await self.session.execute(
            delete(User).where(User.id == user_id)
        )
        return result.rowcount > 0