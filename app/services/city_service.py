from typing import List

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from repositories.city_repository import CityRepository
from schemas.location import CityInput, CityOutput
from repositories.region_repository import RegionRepository
from services.user_service import UserService


class CityService:

    def __init__(self, session: Session):
        self.repository = CityRepository(session)
        self.region_repository = RegionRepository(session)
        self.user_service = UserService(session)

    def create(self, data: CityInput, user_id: UUID4) -> CityOutput:
        if not self.user_service.is_superuser(user_id):
            raise HTTPException(status_code=403, detail="Forbidden")

        if self.repository.city_exists_by_name(data.name):
            raise HTTPException(status_code=400, detail="City already exists")

        if not self.region_repository.region_exists_by_id(data.region_id):
            raise HTTPException(status_code=400, detail="Region not found")

        region = self.region_repository.get_region(data.region_id)
        city = self.repository.create(data)

        return CityOutput(**city.model_dump(exclude_none=True), region=region)

    def get_all_by_region(self, region_id: UUID4) -> List[CityOutput]:
        return self.repository.get_all_by_region(region_id)

    def delete(self, _id: UUID4, user_id: UUID4) -> bool:
        if not self.user_service.is_superuser(user_id):
            raise HTTPException(status_code=403, detail="Forbidden")

        if not self.repository.city_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="City not found")
        city = self.repository.get_by_id(_id)
        return self.repository.delete(city)

    def get_all(self) -> List[CityOutput]:
        return self.repository.get_all()

    def update(self, _id: UUID4, data: CityInput, user_id: UUID4):
        if not self.user_service.is_superuser(user_id):
            raise HTTPException(status_code=403, detail="Forbidden")

        if not self.repository.city_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="City not found")
        city = self.repository.get_by_id(_id)
        updated_city = self.repository.update(city, data)
        return updated_city
