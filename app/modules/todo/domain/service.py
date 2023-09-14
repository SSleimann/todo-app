import abc

from app.kernel.domain.service import BaseService

class ToDoServiceInterface(BaseService, abc.ABC):
    """ Interface for ToDo service """