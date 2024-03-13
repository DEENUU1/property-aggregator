import uuid

from sqlalchemy import Column
from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import UUID

from config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
