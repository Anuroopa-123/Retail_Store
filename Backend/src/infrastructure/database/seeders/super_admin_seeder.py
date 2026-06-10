from sqlalchemy import select

from src.infrastructure.database.postgresql import SessionLocal

from src.domain.entities.user import User
from src.domain.entities.auth.role import Role

from src.infrastructure.auth.security import hash_password


async def seed_super_admin():

    async with SessionLocal() as db:

        existing_user = await db.scalar(
            select(User).where(
                User.email == "superadmin@retail.com"
            )
        )

        if existing_user:
            print("✓ Super Admin already exists")
            return

        role = await db.scalar(
            select(Role).where(
                Role.slug == "super_admin"
            )
        )

        if not role:
            role = Role(
                tenant_id=3,
                name="Super Admin",
                slug="super_admin",
            )

            db.add(role)
            await db.flush()

        user = User(
            tenant_id=3,
            store_id=None,
            email="superadmin@retail.com",
            name="Super Admin",
            password_hash=hash_password(
                "SuperAdmin123"
            ),
            status="active",
        )

        user.roles.append(role)

        db.add(user)

        await db.commit()

        print("✓ Super Admin created")