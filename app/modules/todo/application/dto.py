from pydantic import Field, BaseModel, UUID4

from typing import Optional

from app.kernel.application.dto import EntityDTO
from app.modules.todo.domain.value_objects import StatusValue

class TaskBase(EntityDTO):
    user_id: UUID4 = None

class TaskDTO(TaskBase):
    title: str
    description: str
    status: StatusValue


class TaskCreationDTO(BaseModel):
    title: str
    description: str
    status: StatusValue = Field(default=StatusValue.PENDING)
    user_id: UUID4 = None

class TaskDeletionDTO(TaskBase):
    ...


class TaskGetParamsDTO(TaskBase):
    ...


class TaskUpdatePatchDTO(TaskBase):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusValue] = None


class TaskUpdatePutDTO(TaskBase):
    title: str
    description: str
    status: StatusValue

class TaskGetAllParams(BaseModel):
    user_id: UUID4 = None