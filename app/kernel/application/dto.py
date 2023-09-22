from pydantic import BaseModel, UUID4


class EntityDTO(BaseModel):
    id: UUID4
