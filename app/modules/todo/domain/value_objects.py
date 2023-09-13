import dataclasses

from app.kernel.domain.value_objects import ValueObject

@dataclasses.dataclass(frozen=True)
class StatusValue(ValueObject):
    DONE = "Done"
    PENDING = "Pending"
    CANCELLED = "Cancelled"