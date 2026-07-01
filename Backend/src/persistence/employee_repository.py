from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func
from sqlalchemy.sql.functions import count

from src.domain.entities import user
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
            store_id=data.store_id,
            name=data.name,
            email=data.email,
            password_hash=hash_password(
                data.password
            ),
            status="active"
        )

        self.db.add(user)

        await self.db.flush()
        count = await self.db.scalar(
            select(func.count(EmployeeProfile.id))
        )

        employee_code = f"EMP{count + 1:03d}"

        employee = EmployeeProfile(

    user_id=user.id,

    tenant_id=data.tenant_id,

    store_id=data.store_id,

    employee_code=employee_code,

    gender=data.gender,

    phone=data.phone,

    joining_date=data.joining_date,

    department=str(
        data.department_id
    )
)

        self.db.add(employee)

        await self.db.commit()

        await self.db.refresh(employee)

        return employee