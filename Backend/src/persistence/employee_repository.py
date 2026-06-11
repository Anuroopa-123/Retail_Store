from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.domain.entities.user import User
from src.domain.entities.employee.employee_profile import EmployeeProfile

from src.infrastructure.auth.security import hash_password


class EmployeeRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):

        result = await self.db.execute(
            select(EmployeeProfile)
        )

        return result.scalars().all()

    async def create_employee(
        self,
        data
    ):

        user = User(
            tenant_id=data.tenant_id,
            name=data.name,
            email=data.email,
            password_hash=hash_password(
                data.password
            ),
            status="active"
        )

        self.db.add(user)

        await self.db.flush()

        employee = EmployeeProfile(
            user_id=user.id,
            tenant_id=data.tenant_id,
            employee_code=data.employee_code,
            gender=data.gender,
            phone=data.phone,
            joining_date=data.joining_date,
            department=data.department
        )

        self.db.add(employee)

        await self.db.commit()

        await self.db.refresh(employee)

        return employee