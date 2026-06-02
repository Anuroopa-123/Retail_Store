# src/application/services/core/base_service.py
from __future__ import annotations

from typing import Generic, TypeVar, Union, List, Any
from src.application.pagination import PaginatedResource

Repository = TypeVar("Repository")


class BaseService(Generic[Repository]):

    def __init__(self, repository: Repository) -> None:
        self.repository = repository

    def get_repository(self) -> Repository:
        """Returns the repository instance."""
        return self.repository

    def validate_paginated(
        self,
        result: Union[PaginatedResource, List[Any]],
        model: Any,
    ) -> Union[PaginatedResource, List[Any]]:
        """
        Validates and transforms paginated result or list
        using the provided Pydantic model.

        Usage in service:
            users = await self.repository.get_all_by_tenant(tenant_id)
            return self.validate_paginated(users, UserResponse)
        """
        if isinstance(result, list):
            return [model.model_validate(i) for i in result]

        result.data = [model.model_validate(i) for i in result.data]
        return result