from typing import List

from pydantic import BaseModel, Field, UUID4


class RegionInput(BaseModel):
    name: str


class RegionOutput(BaseModel):
    id: UUID4
    name: str


class CityInput(BaseModel):
    name: str
    region_id: UUID4


class CityOutput(BaseModel):
    id: UUID4
    name: str
    region_id: UUID4
    region: RegionOutput
