from app.kernel.infrastructure.mapper import BaseMapper

from app.modules.user.domain.entities import UserEntity
from app.modules.user.infrastructure.models import UserModel

class UserMapper(BaseMapper):
    def model_to_entity(self, instance: UserModel) -> UserEntity:
        return UserEntity(
            id=instance.id,
            username=instance.username,
            email=instance.email,
            password=instance.password,
            access_token=instance.access_token,
            is_active=instance.is_active
        )
    
    def entity_to_model(self, entity: UserEntity) -> UserModel:
        return UserModel(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            password=entity.password,
            access_token=entity.access_token,
            is_active=entity.is_active
        )
    
