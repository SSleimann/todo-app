from dataclasses import dataclass

from app.kernel.domain.entities import Entity
from app.modules.user.domain.value_objects import Email


@dataclass
class UserEntity(Entity):
    email: Email
    password: str
    access_token: str
    username: str
    is_active: bool
