from typing import Generic, TypeVar

from pydantic import BaseModel, Field

M = TypeVar('M')

class Response(BaseModel, Generic[M]):
    message: str = Field(description="Status message of the response")
    data: M | list[M] = Field(description="List of data or data of entity")
    
