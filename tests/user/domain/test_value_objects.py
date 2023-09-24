from app.modules.user.domain.entities import Email

from email_validator import EmailNotValidError

import pytest

def test_email_value_object():
    email = Email('test@mail.com')
    
    assert email == 'test@mail.com'
    assert isinstance(email, Email)
    
def test_validation_email():
    with pytest.raises(ValueError):
        Email('testmail.com')
    
