from typing import Optional

from pydantic import BaseModel, UUID4

from models.offer import CategoryEnum, BuildingTypeEnum, SubCategoryEnum


class NotificationFilterBase(BaseModel):
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
    user_id: Optional[UUID4] = None


class NotificationFilterInput(NotificationFilterBase):
    pass


class NotificationFilterOutput(NotificationFilterBase):
    id: UUID4


class NotificationFilterUpdateStatus(NotificationFilterBase):
    status: bool
