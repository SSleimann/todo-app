from abc import ABC

from app.kernel.domain.repository import BaseRepository


class ToDoRepository(BaseRepository, ABC):
    """Interface for ToDo repository"""
