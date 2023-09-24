from app.modules.user.infrastructure.mapper import UserMapper
from app.modules.user.infrastructure.models import UserModel
from app.modules.user.domain.entities import UserEntity
from app.modules.user.domain.value_objects import Email

mapper = UserMapper()

def test_mapper_entity_to_model():
    email = Email("testmail@gmail.com")
    
    user_entity = UserEntity(
        id=UserEntity.next_id(),
        email=email,
        password="testpass",
        access_token="akakskaskak",
        is_active=True,
        username="test_user"
    )
    
    user_model = mapper.entity_to_model(user_entity)
    
    assert user_entity.id == user_model.id
    assert user_entity.email == user_model.email
    assert user_entity.password == user_model.password
    assert user_entity.access_token == user_model.access_token
    assert user_entity.is_active == user_model.is_active
    assert user_entity.username == user_model.username
    
def test_mapper_model_to_entity():
    email = Email("testmail@gmail.com")
    
    user_model = UserModel(
        id=UserEntity.next_id(),
        email=email,
        password="testpass",
        access_token="akakskaskak",
        is_active=True,
        username="test_user"
    )
    
    user_entity = mapper.model_to_entity(user_model)
    
    assert user_entity.id == user_model.id
    assert user_entity.email == user_model.email
    assert user_entity.password == user_model.password
    assert user_entity.access_token == user_model.access_token
    assert user_entity.is_active == user_model.is_active
    assert user_entity.username == user_model.username