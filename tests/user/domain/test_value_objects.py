from app.modules.user.domain.entities import Email

from app.kernel.domain.exceptions import AuthErrorException

import pytest


def test_email_value_object():
    email = Email("test@mail.com")

    assert email == "test@mail.com"
    assert isinstance(email, Email)


def test_validation_email():
    with pytest.raises(AuthErrorException):
        Email("testmail.com")
