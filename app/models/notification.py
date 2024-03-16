import uuid

from sqlalchemy import Boolean, Column, ForeignKey, DateTime, func, String
from sqlalchemy.dialects.postgresql import UUID
from config.database import Base
from sqlalchemy.orm import relationship


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    read = Column(Boolean, default=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    user = relationship("User", back_populates="notifications")

    offer_id = Column(UUID(as_uuid=True), ForeignKey('offers.id'))
    offer = relationship("Offer", back_populates="notifications")

