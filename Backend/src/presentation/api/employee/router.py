from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)


from src.infrastructure.database.postgresql import (
    get_session
)

from src.application.services.employee_service import (
    EmployeeService
)

from src.application.models.employee.employee_model import (
    EmployeeCreateRequest
)

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


@router.get("/")
async def list_employees(
    db: AsyncSession = Depends(
        get_session
    )
):

    service = EmployeeService(
        db
    )

    return await service.get_all()

@router.post("/")
async def create_employee(
    payload: EmployeeCreateRequest,
    db: AsyncSession = Depends(get_session)
):

    try:

        service = EmployeeService(db)

        return await service.create(payload)

    except Exception as e:

        print("=================================")
        print("EMPLOYEE CREATE ERROR")
        print(type(e))
        print(e)
        print("=================================")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )