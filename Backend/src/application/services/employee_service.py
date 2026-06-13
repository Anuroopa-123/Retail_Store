from src.persistence.employee_repository import (
    EmployeeRepository
)


class EmployeeService:

    def __init__(self, db):
        self.repository = EmployeeRepository(
            db
        )

    async def get_all(self):
        return await self.repository.get_all()

    async def create(
        self,
        data
    ):
        return await self.repository.create_employee(
            data
        )