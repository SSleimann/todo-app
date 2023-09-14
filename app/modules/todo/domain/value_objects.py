import dataclasses

import enum

class StatusValue(str, enum.Enum):
    DONE: str = "Done"
    PENDING: str = "Pending"
    CANCELLED: str = "Cancelled"
    