# src/persistence/core/base_repository.py
from typing import Any, TypeVar, Optional, List
from fastapi import Depends, Request
from sqlalchemy import select, func, desc, asc, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.postgresql import get_session
from src.application.pagination import create_paginated_resource, PaginatedResource

ModelType = TypeVar("ModelType", bound=Any)


class BaseRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session

    def get_session(self) -> AsyncSession:
        return self.session

    # ── generic CRUD ──────────────────────────────────────────────────────────

    async def get_by_id(self, model, id: int) -> Optional[Any]:
        result = await self.session.execute(
            select(model).where(model.id == id)
        )
        return result.scalar_one_or_none()

    async def create_obj(self, obj: Any) -> Any:
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def save(self, obj: Any) -> Any:
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def delete_obj(self, model, id: int) -> bool:
        result = await self.session.execute(
            delete(model).where(model.id == id)
        )
        return result.rowcount > 0

    async def count(self, model, filters: list = []) -> int:
        query = select(func.count()).select_from(model)
        for f in filters:
            query = query.where(f)
        return await self.session.scalar(query)

    # ── soft delete ───────────────────────────────────────────────────────────

    def with_soft_delete(self, query):
        return query

    # ── pagination ───────────────────────────────────────────────────────────

    async def get_paginated(
        self,
        request: Request,
        query,
        page: int = 1,
        per_page: int = 10,
        sort: Optional[str] = None,
        without_deleted: bool = True,
        with_deleted: bool = False,
        only_deleted: bool = False,
        disable_pagination: bool = False,
    ):
        model = query.column_descriptions[0]["type"]

        if not with_deleted:
            if only_deleted:
                if hasattr(model, "deleted_at"):
                    query = query.where(model.deleted_at.is_not(None))
                elif hasattr(model, "is_deleted"):
                    query = query.where(model.is_deleted.is_(True))
            elif without_deleted:
                if hasattr(model, "deleted_at"):
                    query = query.where(model.deleted_at.is_(None))
                elif hasattr(model, "is_deleted"):
                    query = query.where(model.is_deleted.is_(False))

        for key, value in request.query_params.items():
            if key.startswith("filter[") and key.endswith("]") and value:
                field = key[7:-1]
                if field in ("search", "tab"):
                    continue
                if hasattr(model, field):
                    col = getattr(model, field)
                    col_type = col.property.columns[0].type
                    try:
                        if "," in str(value):
                            values = [v.strip() for v in str(value).split(",")]
                            if "Integer" in str(col_type.__class__):
                                query = query.where(col.in_([int(v) for v in values]))
                            elif "String" in str(col_type.__class__):
                                query = query.where(col.in_(values))
                            elif "Date" in str(col_type.__class__) and len(values) == 2:
                                from datetime import datetime, time
                                def parse_date(v, end_of_day=False):
                                    if "T" in v:
                                        return datetime.fromisoformat(v.replace("Z", "+00:00"))
                                    dt = datetime.strptime(v, "%Y-%m-%d")
                                    if end_of_day:
                                        return datetime.combine(dt.date(), time.max)
                                    return dt
                                query = query.where(col.between(parse_date(values[0]), parse_date(values[1], True)))
                            else:
                                query = query.where(col.in_(values))
                        elif hasattr(col_type, "length") or "String" in str(col_type.__class__):
                            query = query.where(col.ilike(f"%{value}%"))
                        elif "Integer" in str(col_type.__class__):
                            query = query.where(col == int(value))
                        elif "Boolean" in str(col_type.__class__):
                            query = query.where(col == (value.lower() == "true"))
                        else:
                            query = query.where(col == value)
                    except (ValueError, TypeError):
                        query = query.where(col == value)

        if sort:
            sort_desc = sort.startswith("-")
            sort_field = sort.lstrip("-")
            if hasattr(model, sort_field):
                col = getattr(model, sort_field)
                query = query.order_by(desc(col) if sort_desc else asc(col))

        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.session.execute(count_query)).scalar_one()

        if not disable_pagination:
            offset = (page - 1) * per_page
            query = query.offset(offset).limit(per_page)
            items = (await self.session.execute(query)).scalars().all()
            return create_paginated_resource(
                request=request, items=items, total=total, page=page, per_page=per_page
            )

        return (await self.session.execute(query)).scalars().all()