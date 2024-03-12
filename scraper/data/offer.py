from dataclasses import dataclass
from typing import Optional, List

from .location import Location


@dataclass
class Offer:
    title: str
    url: str
    category: Optional[str]
    sub_category: Optional[str]
    building_type: Optional[str] = None
    price: Optional[float] = None
    rent: Optional[float] = None
    description: Optional[str] = None
    price_per_meter: Optional[float] = None
    area: Optional[float] = None
    building_floor: Optional[int] = None
    floor: Optional[int] = None
    room_number: Optional[int] = None
    has_furnitures: Optional[bool] = None
    photos: List[Optional[str]] = None
    location: Optional[Location] = None
