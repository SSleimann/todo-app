from pydantic import Field, BaseModel
from uuid import UUID
from typing import Optional

from app.kernel.application.dto import EntityDTO
from app.modules.todo.domain.value_objects import StatusValue


class TaskDTO(EntityDTO):
    title: str
    description: str
    status: StatusValue
    user_id: UUID


class TaskCreationDTO(BaseModel):
    title: str
    description: str
    status: StatusValue = Field(default=StatusValue.PENDING)


class TaskUpdatePatchDTO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusValue] = None


class TaskUpdatePutDTO(BaseModel):
    title: str
    description: str
    status: StatusValue
