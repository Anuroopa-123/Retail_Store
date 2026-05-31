# src/application/pagination.py
from __future__ import annotations

from typing import TypeVar, Generic, List, Any
from pydantic import BaseModel
from fastapi import Request

T = TypeVar("T")


class PaginatedResource(BaseModel, Generic[T]):
    data: List[Any]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool


def create_paginated_resource(
    request: Request,
    items: list,
    total: int,
    page: int,
    per_page: int,
) -> PaginatedResource:
    total_pages = (total + per_page - 1) // per_page if per_page > 0 else 0
    return PaginatedResource(
        data=items,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1,
    )