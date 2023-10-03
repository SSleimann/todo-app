from email_validator import validate_email, EmailNotValidError
from app.kernel.domain.exceptions import AuthErrorException

class Email(str):
    def __new__(cls, email: str):
        try:
            email = validate_email(email).normalized
        except EmailNotValidError:
            raise AuthErrorException("Invalid email")
        return super().__new__(cls, email)
