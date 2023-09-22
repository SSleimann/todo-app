from dataclasses import dataclass

from app.kernel.domain.entities import Entity
from app.modules.todo.domain.value_objects import StatusValue


@dataclass
class TaskEntity(Entity):
    title: str
    description: str
    status: StatusValue
