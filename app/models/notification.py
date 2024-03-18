import uuid

from sqlalchemy import Boolean, Column, ForeignKey, DateTime, func, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from config.database import Base

notification_offer_association = Table(
    'notification_offer_association',
    Base.metadata,
    Column('notification_id', UUID(as_uuid=True), ForeignKey('notifications.id')),
    Column('offer_id', UUID(as_uuid=True), ForeignKey('offers.id'))
)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=True)
    message = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    read = Column(Boolean, default=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    user = relationship("User", back_populates="notifications")
    offers = relationship("Offer", secondary=notification_offer_association, back_populates="notifications")
