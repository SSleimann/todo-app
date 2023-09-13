import abc

from app.kernel.domain.service import BaseService

class ToDoService(BaseService, abc.ABC):
    """ Interface for ToDo service """