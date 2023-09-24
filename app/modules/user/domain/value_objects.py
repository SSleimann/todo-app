from email_validator import validate_email, EmailNotValidError


class Email(str):
    def __new__(cls, email: str):
        try:
            email = validate_email(email).normalized
        except EmailNotValidError:
            raise ValueError("Invalid email")
        return super().__new__(cls, email)
