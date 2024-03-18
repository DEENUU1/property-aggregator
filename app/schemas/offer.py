from typing import List, Dict, Any, Optional

from pydantic import BaseModel, UUID4

from models.offer import SubCategoryEnum, BuildingTypeEnum, CategoryEnum
from schemas.location import CityOutput
from schemas.photo import PhotoInput
from datetime import datetime


class OfferInput(BaseModel):
    title: str
    details_url: str
    category: CategoryEnum
    sub_category: SubCategoryEnum
    building_type: Optional[BuildingTypeEnum] = None
    price: Optional[float] = None
    rent: Optional[float] = None
    description: Optional[str] = None
    price_per_m: Optional[float] = None
    area: Optional[float] = None
    building_floot: Optional[int] = None
    floor: Optional[int] = None
    rooms: Optional[int] = None
    furniture: Optional[bool] = None
    photos: List[PhotoInput]
    city_id: UUID4


class OfferScraper(BaseModel):
    title: str
    details_url: str
    category: CategoryEnum
    sub_category: SubCategoryEnum
    building_type: Optional[BuildingTypeEnum] = None
    price: Optional[float] = None
    rent: Optional[float] = None
    description: Optional[str] = None
    price_per_m: Optional[float] = None
    area: Optional[float] = None
    building_floot: Optional[int] = None
    floor: Optional[int] = None
    rooms: Optional[int] = None
    furniture: Optional[bool] = None
    photos: List[PhotoInput]
    region_name: str
    city_name: str


class OfferOutput(BaseModel):
    id: UUID4
    title: str
    details_url: str
    category: CategoryEnum
    sub_category: SubCategoryEnum
    building_type: BuildingTypeEnum | None
    price: Optional[float] = None
    rent: Optional[float] = None
    description: Optional[str] = None
    price_per_m: Optional[float] = None
    area: Optional[float] = None
    building_floot: Optional[int] = None
    floor: Optional[int] = None
    rooms: Optional[int] = None
    furniture: Optional[bool] = None
    photos: List[PhotoInput]
    city: CityOutput
    created_at: datetime
    updated_at: datetime


class OfferList(BaseModel):
    page: int
    page_size: int
    offers: List[Dict[str, Any]]
