from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.models.department.department_model import DepartmentCreateRequest
from src.infrastructure.database.postgresql import get_session
from src.domain.entities.department.department import Department

router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)

@router.get("/")
async def list_departments(
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(Department)
    )

    return result.scalars().all()


@router.post("/")
async def create_department(
    body: DepartmentCreateRequest,
    db: AsyncSession = Depends(
        get_session
    )
):

    department = Department(

        name=body.name,

        tenant_id=
        body.tenant_id,

        store_id=
        body.store_id,

        created_by=
        body.created_by
    )

    db.add(department)

    await db.commit()

    await db.refresh(
        department
    )

    return department



@router.get(
    "/tenant/{tenant_id}/store/{store_id}"
)
async def list_department_by_store(

    tenant_id: int,
    store_id: int,

    db: AsyncSession =
    Depends(get_session)

):

    result = await db.execute(

        select(Department)

        .where(
            Department.tenant_id
            == tenant_id,

            Department.store_id
            == store_id
        )
    )

    return result.scalars().all()