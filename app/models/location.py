import uuid

from sqlalchemy import Column, String, FLOAT
from sqlalchemy.dialects.postgresql import UUID

from config.database import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city = Column(String)
    region = Column(String)
    lat = Column(FLOAT)
    lon = Column(FLOAT)
