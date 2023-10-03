import uuid

from sqlalchemy import Column, Text, String, Enum, ForeignKey

from app.config.database import GUID, Base
from app.modules.todo.domain.value_objects import StatusValue

class TaskModel(Base):
    __tablename__ = "tasks"
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True, default="Task")
    status = Column(Enum(StatusValue), nullable=False, default=StatusValue.PENDING)
    user_id = Column(GUID, ForeignKey("users.id"), nullable=False)