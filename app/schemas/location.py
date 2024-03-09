from typing import List

from pydantic import BaseModel, UUID, Field


class RegionInput(BaseModel):
    name: str


class CityInput(BaseModel):
    name: str
    region_id: UUID


class RegionOutput(BaseModel):
    id: UUID
    name: str
    cities: List["CityOutput"] = Field(default_factory=list)


class CityOutput(BaseModel):
    id: UUID
    name: str
    region_id: UUID
    region: RegionOutput
