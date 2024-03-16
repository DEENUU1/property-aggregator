from typing import Optional

from pydantic import BaseModel

from models.offer import CategoryEnum, BuildingTypeEnum, SubCategoryEnum


class NotificationBase(BaseModel):
    category: Optional[CategoryEnum] = None
    sub_category: Optional[SubCategoryEnum] = None
    building_type: Optional[BuildingTypeEnum] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    area_min: Optional[float] = None
    area_max: Optional[float] = None
    rooms: Optional[int] = None
    furniture: Optional[bool] = None
    floor: Optional[bool] = None
    query: Optional[str] = None
    active: bool = True


class NotificationInput(NotificationBase):


class NotificationOutput(NotificationBase):


class NotificationUpdateStatus(BaseModel):
    active: Optional[bool] = None
