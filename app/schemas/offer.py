from typing import List

from pydantic import BaseModel, UUID, Field

from models.offer import SubCategoryEnum, BuildingTypeEnum, CategoryEnum
from schemas.location import CityOutput
from schemas.photo import PhotoInput, PhotoOutput


class OfferInput(BaseModel):
    title: str
    details_url: str
    category: CategoryEnum
    sub_category: SubCategoryEnum
    building_type: BuildingTypeEnum | None
    price: float | None
    rent: float | None
    description: str | None
    price_per_m: float | None
    area: float | None
    building_floor: int | None
    floor: int | None
    rooms: int | None
    furniture: bool | None
    photos: List[PhotoInput] | None
    city_id: UUID


class OfferOutput(BaseModel):
    id: UUID
    title: str
    details_url: str
    category: CategoryEnum
    sub_category: SubCategoryEnum
    building_type: BuildingTypeEnum | None
    price: float | None
    rent: float | None
    description: str | None
    price_per_m: float | None
    area: float | None
    building_floor: int | None
    floor: int | None
    rooms: int | None
    furniture: bool | None
    photos: List[PhotoOutput] = Field(default_factory=list)
    city_id: UUID
    city: CityOutput = None
