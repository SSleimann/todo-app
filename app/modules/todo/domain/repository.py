from abc import ABC, abstractmethod

from app.kernel.domain.repository import BaseRepository
from app.modules.todo.domain.entities import TaskEntity


class ToDoRepository(BaseRepository, ABC):
    """Interface for ToDo repository"""

    @abstractmethod
    async def get_all_paginated_with_params(
        self, params: dict, page: int = 1, per_page: int = 10
    ) -> list[TaskEntity]:
        """Get all tasks with params"""
        raise NotImplementedError
