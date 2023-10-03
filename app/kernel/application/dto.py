from pydantic import BaseModel
from uuid import UUID

class EntityDTO(BaseModel):
    id: UUID
