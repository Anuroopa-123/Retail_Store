from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from src.domain.entities.user import User
from src.domain.entities.employee.employee_profile import EmployeeProfile
from src.infrastructure.auth.security import hash_password


class EmployeeRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(
        self,
        tenant_id: int,
        store_id: int
    ):

        result = await self.db.execute(

            select(EmployeeProfile)
            .options(
                joinedload(EmployeeProfile.user)
            )
            .where(
                EmployeeProfile.tenant_id == tenant_id,
                EmployeeProfile.store_id == store_id
            )

        )

        employees = result.scalars().all()

        return [

            {
                "id": emp.id,
                "employee_code": emp.employee_code,
                "name": emp.user.name if emp.user else "",
                "email": emp.user.email if emp.user else "",
                "phone": emp.phone,
                "gender": emp.gender,
                "department": emp.department,
                "joining_date": emp.joining_date,
                "tenant_id": emp.tenant_id,
                "store_id": emp.store_id,
                "status": emp.user.status if emp.user else ""
            }

            for emp in employees

        ]

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

        total = await self.db.scalar(

            select(func.count(EmployeeProfile.id))

        )

        employee_code = f"EMP{total + 1:03d}"

        employee = EmployeeProfile(

            user_id=user.id,
            tenant_id=data.tenant_id,
            store_id=data.store_id,
            employee_code=employee_code,
            gender=data.gender,
            phone=data.phone,
            joining_date=data.joining_date,
            department=str(data.department_id)

        )

        self.db.add(employee)

        await self.db.commit()

        await self.db.refresh(employee)

        return employee