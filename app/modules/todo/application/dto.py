from pydantic import Field, BaseModel

from typing import Optional

from app.kernel.application.dto import EntityDTO
from app.modules.todo.domain.value_objects import StatusValue

class TaskDTO(EntityDTO):
    title: str
    description: str
    status: StatusValue = Field(default=StatusValue.PENDING)

class TaskCreationDTO(BaseModel):
    title: str
    description: str
    status: StatusValue = Field(default=StatusValue.PENDING)
    

class TaskDeletionDTO(EntityDTO):
    ...

class TaskGetDTO(EntityDTO):
    ...

class TaskUpdateDTO(EntityDTO):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusValue] = None
    
class TaskSetStatusValueDTO(EntityDTO):
    status: StatusValue