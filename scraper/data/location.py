from dataclasses import dataclass
from typing import Optional


@dataclass
class Location:
    region: Optional[str] = None
    city: Optional[str] = None
