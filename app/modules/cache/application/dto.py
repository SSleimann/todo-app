from pydantic import BaseModel

from app.kernel.application.dto import EntityDTO

class CacheDataDTO(EntityDTO):
    data: bytes

class AddToCacheDTO(CacheDataDTO):
    data: bytes
    
class UpdateToCacheDTO(BaseModel):
    data: bytes