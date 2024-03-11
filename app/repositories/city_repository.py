from typing import List, Optional, Type

from pydantic import UUID4
from sqlalchemy.orm import Session

from models.location import City
from schemas.location import CityInput, CityOutput, RegionOutput


class CityRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, data: CityInput) -> CityInput:
        city = City(**data.model_dump(exclude_none=True))
        self.session.add(city)
        self.session.commit()
        self.session.refresh(city)
        return CityInput(**city.__dict__)

    def get_all(self) -> List[Optional[CityOutput]]:
        cities = self.session.query(City).all()
        return [
            CityOutput(
                id=city.id,
                name=city.name,
                region=RegionOutput(
                    id=city.region.id, name=city.region.name
                )
            )
            for city in cities
        ]

    def get_by_id(self, _id: UUID4) -> Type[City]:
        return self.session.query(City).filter_by(id=_id).first()

    def get_by_name(self, name: str) -> Type[City]:
        return self.session.query(City).filter_by(name=name).first()

    def city_exists_by_name(self, name: str) -> bool:
        city = self.session.query(City).filter_by(name=name).first()
        if city:
            return True
        return False

    def city_exists_by_id(self, _id: UUID4) -> bool:
        city = self.session.query(City).filter_by(id=_id).first()
        if city:
            return True
        return False

    # TODO update

    def delete(self, city: Type[City]) -> bool:
        self.session.delete(city)
        self.session.commit()
        return True
