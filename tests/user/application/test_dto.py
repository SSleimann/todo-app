from pytest import raises

from app.modules.user.application.dto import UserCreationDTO

def test_invalid_password_dto():
    with raises(ValueError):
        UserCreationDTO(
            username='xxxxx',
            password='xxx',
            confirm_password='xxxxx',
            email='pepito@email.com'
        )