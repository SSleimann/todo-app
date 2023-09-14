import enum
from pydantic import BaseModel

class A(BaseModel):
    hola: str
    
e = A(hola='1')

print(e.model_dump())