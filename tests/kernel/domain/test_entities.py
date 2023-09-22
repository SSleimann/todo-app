from dataclasses import dataclass

from app.kernel.domain.entities import Entity


@dataclass
class UserEntity(Entity):
    name: str


def test_entity():
    e = UserEntity(id=UserEntity.next_id(), name="test")
    assert e.id is not None
    assert e.name == "test"
