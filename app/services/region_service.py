from sqlalchemy.orm import Session

from repositories.region_repository import RegionRepository
from schemas.location import RegionInput, RegionOutput
from typing import List, Optional
from config.database import NotFoundError, AlreadyExistsError
from pydantic import UUID4


class RegionService:

    def __init__(self, session: Session):
        self.repository = RegionRepository(session)

    def create(self, data: RegionInput) -> RegionInput:
        if self.repository.region_exists_by_name(data.name):
            raise AlreadyExistsError("Region already exists")
        return self.repository.create(data)

    def get_all(self) -> List[Optional[RegionOutput]]:
        return self.repository.get_all()

    def delete(self, _id: UUID4) -> bool:
        if not self.repository.region_exists_by_id(_id):
            raise NotFoundError("Region not found")

        region = self.repository.get_by_id(_id)
        self.repository.delete(region)
        return True

    def update(self, _id: UUID4, data: RegionInput) -> RegionInput:
        if not self.repository.region_exists_by_id(_id):
            raise NotFoundError("Region not found")

        region = self.repository.get_by_id(_id)
        return self.repository.update(region, data)
