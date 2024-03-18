from pydantic import BaseModel, UUID4


class RegionInput(BaseModel):
    name: str


class RegionOutput(BaseModel):
    id: UUID4
    name: str


class CityInput(BaseModel):
    name: str
    region_id: UUID4


class CityInDb(BaseModel):
    id: UUID4
    name: str
    region_id: UUID4

    class Config:
        orm_mode = True


class CityOutput(BaseModel):
    id: UUID4
    name: str
    region: RegionOutput

