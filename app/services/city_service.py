from sqlalchemy.orm import Session

from repositories.city_repository import CityRepository
from schemas.location import CityInput, CityOutput
from typing import List
from config.database import NotFoundError, AlreadyExistsError
from pydantic import UUID4


class CityService:

    def __init__(self, session: Session):
        self.repository = CityRepository(session)

    def create(self, data: CityInput) -> CityInput:
        if self.repository.city_exists_by_name(data.name):
            raise AlreadyExistsError("City already exists")
        return self.repository.create(data)

    def get_all(self) -> List[CityOutput]:
        return self.repository.get_all()

    def delete(self, _id: UUID4) -> bool:
        if not self.repository.city_exists_by_id(_id):
            raise NotFoundError("City not found")

        city = self.repository.get_by_id(_id)
        return self.repository.delete(city)


