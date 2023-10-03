from pydantic import BaseModel, EmailStr, SecretStr, model_validator

from app.kernel.application.dto import EntityDTO

class UserDTO(EntityDTO):
    email: EmailStr
    username: str
    is_active: bool
    access_token: str | None


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


class UserGetDTO(EntityDTO):
    ...


class UserGetByEmailDTO(BaseModel):
    email: EmailStr


class UserGetByAccessTokenDTO(BaseModel):
    access_token: str


class LoginDTO(BaseModel):
    email: EmailStr
    password: SecretStr


class TokenDTO(BaseModel):
    access_token: str
    token_type: str
