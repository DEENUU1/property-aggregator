import uuid

from sqlalchemy import Column, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from config.database import Base


class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=func.now())
    filter_id = Column(UUID(as_uuid=True), ForeignKey('notifications_filters.id'), unique=True)

    filter = relationship("NotificationFilter", back_populates="notification")
