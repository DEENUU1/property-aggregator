import uuid
from enum import Enum

from sqlalchemy import Column, Integer, String, FLOAT, Boolean, ForeignKey, DateTime, func
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from config.database import Base
from models.notification import notification_offer_association


class CategoryEnum(str, Enum):
    """
    Enumeration for categories.
    """
    MIESZKANIE = "Mieszkanie"  # or kawalerka
    POKOJ = "Pokój"
    DOM = "Dom"
    DZIALKA = "DZIAŁKA"
    BIURA_I_LOKALE = "Biura i lokale"
    GARAZE_I_PARKINGI = "Garaże i parkingi"
    STANCJE_I_POKOJE = "Stancje i pokoje"
    HALE_I_MAGAZYNY = "Hale i magazyny"
    POZOSTALE = "Pozostałe"  # Inwestycje


class BuildingTypeEnum(str, Enum):
    """
    Enumeration for types of buildings.
    """
    APARTAMENTOWIEC = "Apartamentowiec"
    BLOK = "Blok"
    KAMIENICA = "Kamienica"
    POZOSTALE = "Pozostałe"
    LOFT = "Loft"


class SubCategoryEnum(str, Enum):
    """
    Enumeration for subcategories.
    """
    WYNAJEM = "Wynajem"
    SPRZEDAZ = "Sprzedaż"


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
    building_floot = Column(Integer, nullable=True)  # TODO change this to floor typo
    floor = Column(Integer, nullable=True)
    rooms = Column(Integer, nullable=True)
    furniture = Column(Boolean, nullable=True)
    city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"))
    city = relationship("City", back_populates="offers")
    photos = relationship("Photo", back_populates="offer")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    favorited_by = relationship("Favorite", back_populates="offer")
    notifications = relationship(
        "Notification",
        secondary=notification_offer_association,
        back_populates="offers"
    )
