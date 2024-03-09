from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Location:
    region: Optional[str] = None
    city: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None


@dataclass
class Offer:
    title: str
    url: str
    category: Optional[str] = None
    sub_category: Optional[str] = None
    building_type: Optional[str] = None

    location: Optional[Location] = None
    photos: List[Optional[str]] = None
    price: Optional[float] = None
    rent: Optional[float] = None
    description: Optional[str] = None

    price_per_meter: Optional[float] = None
    area: Optional[float] = None
    building_floor: Optional[int] = None
    floor: Optional[float] = None
    room_number: Optional[int] = None
    has_furnitures: Optional[bool] = None
