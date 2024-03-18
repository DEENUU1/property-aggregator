from sqlalchemy.orm import Session
from fastapi import HTTPException
from repositories.region_repository import RegionRepository
from schemas.location import RegionInput, RegionOutput
from typing import List, Optional
from pydantic import UUID4
from services.user_service import UserService


class RegionService:

    def __init__(self, session: Session):
        self.repository = RegionRepository(session)
        self.user_service = UserService(session)

    def create(self, data: RegionInput, user_id: UUID4) -> RegionOutput:
        if not self.user_service.is_superuser(user_id):
            raise HTTPException(status_code=403, detail="Forbidden")

        if self.repository.region_exists_by_name(data.name):
            raise HTTPException(status_code=400, detail="Region already exists")
        return self.repository.create(data)

    def get_all(self) -> List[Optional[RegionOutput]]:
        return self.repository.get_all()

    def delete(self, _id: UUID4, user_id: UUID4) -> bool:
        if not self.user_service.is_superuser(user_id):
            raise HTTPException(status_code=403, detail="Forbidden")

        if not self.repository.region_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Region not found")

        region = self.repository.get_by_id(_id)
        self.repository.delete(region)
        return True

    def update(self, _id: UUID4, data: RegionInput, user_id: UUID4) -> RegionInput:
        if not self.user_service.is_superuser(user_id):
            raise HTTPException(status_code=403, detail="Forbidden")

        if not self.repository.region_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Region not found")

        region = self.repository.get_by_id(_id)
        return self.repository.update(region, data)
