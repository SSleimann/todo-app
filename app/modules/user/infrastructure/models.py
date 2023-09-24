import uuid

from sqlalchemy import Column, String, Boolean

from app.config.database import GUID, Base


class UserModel(Base):
    __tablename__ = "users"
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    access_token = Column(String(255), nullable=False, unique=True)
    username = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
