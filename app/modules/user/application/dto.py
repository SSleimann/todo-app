from pydantic import BaseModel, EmailStr, SecretStr, model_validator, Field
from datetime import datetime
from uuid import UUID

from app.kernel.application.dto import EntityDTO


class UserDTO(EntityDTO):
    email: EmailStr
    username: str
    is_active: bool
    access_token: str | None
    task_count: int = 0


class UserCreationDTO(BaseModel):
    email: EmailStr
    password: SecretStr
    confirm_password: SecretStr
    username: str

    @model_validator(mode="after")
    def validate_password_match(self):
        paswd1 = self.password
        paswd2 = self.confirm_password

        if paswd1 is not None and paswd2 is not None and paswd1 != paswd2:
            raise ValueError("Passwords do not match")

        return self


class LoginDTO(BaseModel):
    email: EmailStr
    password: SecretStr


class TokenDTO(BaseModel):
    access_token: str
    token_type: str


class UserCodeDTO(BaseModel):
    user_id: UUID
    code: bytes
    expiration_time: datetime = Field(description="Expiration time in seconds")
