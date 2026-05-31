# src/application/services/user_service.py
from __future__ import annotations

from datetime import datetime, timezone
from http.client import HTTPException
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.core.base_service import BaseService
from src.persistence.user_repository import UserRepository
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
    TokenExpiredError,
    TokenInvalidError,
    UserNotFoundError,
    TenantAccessError,
)


class UserService(BaseService[UserRepository]):
    """
    Service layer for user operations.

    Responsibilities:
    - Orchestrate repository calls with business logic
    - Own token validation logic (expiry, replay checks) before delegating writes
    - Raise domain errors early so controllers stay clean

    The service intentionally wraps repository methods even when the call is a
    pass-through: this keeps the controller decoupled from persistence and gives
    a clear place to add cross-cutting concerns (logging, events, etc.) later.
    """

    def __init__(self, session: AsyncSession) -> None:
        repository = UserRepository(session)
        super().__init__(repository)
        self.session = session

    # ── CRUD ──────────────────────────────────────────────────────────────────

    async def register(self, data: UserCreateModel):
        return await self.repository.create(data)

    async def get_by_id(self, user_id: int):
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return user

    async def get_by_email(self, email: str):
        user = await self.repository.get_by_email(email)
        if not user:
            raise UserNotFoundError()
        return user

    async def get_all_by_tenant(
        self,
        tenant_id: int,
        store_id: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ):
        return await self.repository.get_all_by_tenant(
            tenant_id=tenant_id,
            store_id=store_id,
            limit=limit,
            offset=offset,
        )

    async def update(self, user_id: int, data: UserUpdateModel):
        # Service owns the existence check; repository.update trusts user exists.
        await self.get_by_id(user_id)
        return await self.repository.update(user_id, data)
    
    async def get_password_reset_token(self, token_hash: str):
        return await self.repository.get_password_reset_token(token_hash)

    async def delete_password_reset_token(self, user_id: int):
        return await self.repository.delete_password_reset_token(user_id)

    async def change_password(self, user_id: int, data: UserPasswordUpdateModel):
        return await self.repository.update_password(user_id, data)

    async def update_status(self, user_id: int, data: UserStatusUpdateModel):
        return await self.repository.update_status(user_id, data)

    # ── Roles ─────────────────────────────────────────────────────────────────

    # src/application/services/user_service.py

# CHANGED: added current_tenant_id parameter
# tenant validation now lives here so any caller is protected
    async def assign_role(
        self,
        user_id: int,
        data: AssignRoleBySlugModel,
        current_tenant_id: int,          # ← ADDED: tenant context from router
    ):
        target_user = await self.get_by_id(user_id)  # raises UserNotFoundError if not found

        if target_user.tenant_id != current_tenant_id:
            raise TenantAccessError()    # ← domain exception, not HTTPException

        return await self.repository.assign_role_by_slug(user_id, data)


    async def assign_roles(self, user_id: int, data: AssignRolesModel):
        return await self.repository.assign_roles(user_id, data)

    async def remove_role(self, user_id: int, data: AssignRoleBySlugModel):
        return await self.repository.remove_role(user_id, data)

    async def assign_roles(self, user_id: int, data: AssignRolesModel):
        return await self.repository.assign_roles(user_id, data)

    async def remove_role(self, user_id: int, data: AssignRoleBySlugModel):
        return await self.repository.remove_role(user_id, data)

    # ── Email verification ────────────────────────────────────────────────────

    async def verify_email(self, token_hash: str):
        """
        Validate token business rules here; delegate the DB write to the
        repository. This prevents the repository from duplicating validation
        logic and makes the rules easy to test in isolation.
        """
        token = await self.repository.get_email_verification_token(token_hash)
        if not token:
            raise TokenInvalidError()
        if token.verified_at:
            # Token already consumed — replay attempt.
            raise TokenInvalidError()
        if token.expires_at < datetime.now(timezone.utc):
            raise TokenExpiredError()

        return await self.repository.verify_email(token_hash)

    # ── Password reset tokens ─────────────────────────────────────────────────

    async def create_password_reset_token(
        self, user_id: int, token_hash: str, expires_at: datetime
    ):
        return await self.repository.create_password_reset_token(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )

    # ── Email verification tokens ─────────────────────────────────────────────

    async def create_email_verification_token(
        self, user_id: int, token_hash: str, expires_at: datetime
    ):
        return await self.repository.create_email_verification_token(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )

    # ── Personal access tokens ────────────────────────────────────────────────

    async def get_personal_access_tokens(self, user_id: int):
        return await self.repository.get_personal_access_tokens(user_id)

    async def create_personal_access_token(
        self,
        user_id: int,
        name: str,
        token_hash: str,
        abilities: list,
        expires_at: Optional[datetime] = None,
    ):
        return await self.repository.create_personal_access_token(
            user_id=user_id,
            name=name,
            token_hash=token_hash,
            abilities=abilities,
            expires_at=expires_at,
        )

    async def delete_personal_access_token(
        self, user_id: int, token_id: int
    ) -> bool:
        return await self.repository.delete_personal_access_token(
            user_id=user_id,
            token_id=token_id,
        )

    # ── Delete ────────────────────────────────────────────────────────────────

    async def soft_delete(self, user_id: int) -> bool:
        """
        Deactivate a user. Delegates through update_status so any validation
        on allowed status values is applied consistently.
        """
        await self.update_status(user_id, UserStatusUpdateModel(status="inactive"))
        return True

    async def force_delete(self, user_id: int) -> bool:
        return await self.repository.force_delete(user_id)