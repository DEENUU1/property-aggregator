import uuid
from enum import Enum

from sqlalchemy import Column, Integer, String, FLOAT, Boolean, ForeignKey
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from config.database import Base


class CategoryEnum(str, Enum):
    MIESZKANIE = "Mieszkanie"


class SubCategoryEnum(str, Enum):
    WYNAJEM = "Wynajem"


class BuildingTypeEnum(str, Enum):
    BLOK = "Blok"


class Offer(Base):
    __tablename__ = "offers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    details_url = Column(String, unique=True, nullable=False)
    category = Column(SQLAlchemyEnum(CategoryEnum), nullable=False)
    sub_category = Column(SQLAlchemyEnum(SubCategoryEnum), nullable=False)
    building_type = Column(SQLAlchemyEnum(BuildingTypeEnum), nullable=True)
    price = Column(FLOAT, nullable=True)
    rent = Column(FLOAT, nullable=True)
    description = Column(String, nullable=True)
    price_per_m = Column(FLOAT, nullable=True)
    area = Column(FLOAT, nullable=True)
    building_floot = Column(Integer, nullable=True)  # todo change this to floor typo
    floor = Column(Integer, nullable=True)
    rooms = Column(Integer, nullable=True)
    furniture = Column(Boolean, nullable=True)
    photos = relationship("Photo", back_populates="offer", cascade="all, delete-orphan")
    city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"))
    city = relationship("City", back_populates="offers")
