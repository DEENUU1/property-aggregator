from typing import List

from pydantic import BaseModel, UUID4

from models.offer import SubCategoryEnum, BuildingTypeEnum, CategoryEnum
from schemas.location import CityOutput
from schemas.photo import PhotoInput


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
    building_floot: int | None
    floor: int | None
    rooms: int | None
    furniture: bool | None
    photos: List[PhotoInput]
    # city_id: UUID4


class OfferOutput(BaseModel):
    id: UUID4
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
    building_floot: int | None
    floor: int | None
    rooms: int | None
    furniture: bool | None
    photos: List[PhotoInput]
    # city_id: UUID4
    # city: CityOutput = None
