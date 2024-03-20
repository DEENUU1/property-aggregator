import uuid

from sqlalchemy import String, Boolean, Column, Float, Integer, ForeignKey
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from config.database import Base
from .offer import SubCategoryEnum, CategoryEnum, BuildingTypeEnum
from sqlalchemy.orm import relationship


class NotificationFilter(Base):
    __tablename__ = 'notifications_filters'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = Column(SQLAlchemyEnum(CategoryEnum), nullable=True)
    sub_category = Column(SQLAlchemyEnum(SubCategoryEnum), nullable=True)
    building_type = Column(SQLAlchemyEnum(BuildingTypeEnum), nullable=True)
    price_min = Column(Float, nullable=True)
    price_max = Column(Float, nullable=True)
    area_min = Column(Float, nullable=True)
    area_max = Column(Float, nullable=True)
    rooms = Column(Integer, nullable=True)
    furniture = Column(Boolean, nullable=True)
    floor = Column(Integer, nullable=True)
    query = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    user = relationship("User", back_populates="notifications_filters")
