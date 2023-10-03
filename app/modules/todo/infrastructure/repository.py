from sqlalchemy import select

from app.kernel.infrastructure.repository import SQLAlchemyRepository
from app.modules.todo.domain.entities import TaskEntity
from app.modules.todo.domain.repository import ToDoRepository
from app.modules.todo.infrastructure.mapper import TaskMapper
from app.modules.todo.infrastructure.models import TaskModel


class SQLToDoRepository(ToDoRepository, SQLAlchemyRepository):
    mapper_class = TaskMapper
    model_class = TaskModel

    async def get_all_paginated_with_params(
        self, params: dict, page: int = 1, per_page: int = 10
    ) -> list[TaskEntity]:
        model_class = self.get_model_class()
        filter_params = {
            key: value for key, value in params.items() if hasattr(model_class, key)
        }

        limit = per_page * page
        offset = (page - 1) * per_page

        instances = await self._session.scalars(
            select(model_class).filter_by(**filter_params).limit(limit).offset(offset)
        )

        entities = [self.model_to_entity(instance) for instance in instances.all()]

        return entities
