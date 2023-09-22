from dataclasses import dataclass

from app.kernel.domain.value_objects import ValueUUID


@dataclass
class Entity:
    id: ValueUUID

    @staticmethod
    def next_id() -> ValueUUID:
        return ValueUUID.next_id()
