import uuid

from sqlalchemy import Column, ForeignKey, UUID
from sqlalchemy.orm import relationship

from config.database import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    offer_id = Column(UUID(as_uuid=True), ForeignKey("offers.id"))

    user = relationship("User", back_populates="favorites")
    offer = relationship("Offer", back_populates="favorited_by")
