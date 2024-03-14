from typing import List

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from repositories.city_repository import CityRepository
from schemas.location import CityInput, CityOutput


class CityService:

    def __init__(self, session: Session):
        self.repository = CityRepository(session)

    def create(self, data: CityInput) -> CityInput:
        if self.repository.city_exists_by_name(data.name):
            raise HTTPException(status_code=400, detail="City already exists")
        return self.repository.create(data)

    def get_all_by_region(self, region_id: UUID4) -> List[CityOutput]:
        return self.repository.get_all_by_region(region_id)

    def delete(self, _id: UUID4) -> bool:
        if not self.repository.city_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="City not found")
        city = self.repository.get_by_id(_id)
        return self.repository.delete(city)

    def get_all(self) -> List[CityOutput]:
        return self.repository.get_all()

    def update(self, _id: UUID4, data: CityInput):
        if not self.repository.city_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="City not found")
        city = self.repository.get_by_id(_id)
        updated_city = self.repository.update(city, data)
        return updated_city
