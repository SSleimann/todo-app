from pydantic import Field, BaseModel, UUID4

from typing import Optional

from app.kernel.application.dto import EntityDTO
from app.modules.todo.domain.value_objects import StatusValue


class TaskDTO(EntityDTO):
    title: str
    description: str
    status: StatusValue


class TaskCreationDTO(BaseModel):
    title: str
    description: str
    status: StatusValue = Field(default=StatusValue.PENDING)


class TaskDeletionDTO(EntityDTO):
    ...


class TaskGetDTO(EntityDTO):
    ...


class TaskUpdatePatchDTO(EntityDTO):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusValue] = None


class TaskUpdatePutDTO(EntityDTO):
    title: str
    description: str
    status: StatusValue
