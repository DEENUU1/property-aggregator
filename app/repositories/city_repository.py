from typing import List, Optional, Type

from pydantic import UUID4
from sqlalchemy.orm import Session

from models.location import City
from schemas.location import CityInput, CityOutput, RegionOutput, CityInDb


class CityRepository:
    """
    Repository class for handling cities.
    """

    def __init__(self, session: Session):
        """
        Initialize the repository with a database session.

        Args:
            session (Session): The database session.
        """
        self.session = session

    def create(self, data: CityInput) -> CityInDb:
        """
        Create a new city.

        Args:
            data (CityInput): The city data.

        Returns:
            CityInDb: The created city.
        """
        city = City(**data.model_dump(exclude_none=True))
        self.session.add(city)
        self.session.commit()
        self.session.refresh(city)
        return CityInDb(**city.__dict__)

    def get_all(self) -> List[Optional[CityOutput]]:
        """
        Get all cities.

        Returns:
            List[Optional[CityOutput]]: A list of city outputs.
        """
        cities = self.session.query(City).all()
        return self._map_city_to_schema_list(cities)

    def get_all_by_region(self, region_id: UUID4) -> List[Optional[CityOutput]]:
        """
        Get all cities by region.

        Args:
            region_id (UUID4): The region ID.

        Returns:
            List[Optional[CityOutput]]: A list of city outputs.
        """
        cities = self.session.query(City).filter_by(region_id=region_id).all()
        return self._map_city_to_schema_list(cities)

    @staticmethod
    def _map_city_to_schema_list(cities: List[Type[City]]) -> List[CityOutput]:
        """
        Map cities to CityOutput schema.

        Args:
            cities (List[Type[City]]): List of City instances.

        Returns:
            List[CityOutput]: List of CityOutput instances.
        """
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
        """
        Get city by ID.

        Args:
            _id (UUID4): The city ID.

        Returns:
            Type[City]: The city instance.
        """
        return self.session.query(City).filter_by(id=_id).first()

    def get_by_name(self, name: str) -> Type[City]:
        """
        Get city by name.

        Args:
            name (str): The city name.

        Returns:
            Type[City]: The city instance.
        """
        return self.session.query(City).filter_by(name=name).first()

    def city_exists_by_name(self, name: str) -> bool:
        """
        Check if a city exists by name.

        Args:
            name (str): The city name.

        Returns:
            bool: True if the city exists, False otherwise.
        """
        city = self.session.query(City).filter_by(name=name).first()
        return bool(city)

    def city_exists_by_id(self, _id: UUID4) -> bool:
        """
        Check if a city exists by ID.

        Args:
            _id (UUID4): The city ID.

        Returns:
            bool: True if the city exists, False otherwise.
        """
        city = self.session.query(City).filter_by(id=_id).first()
        return bool(city)

    def update(self, city: Type[City], data: CityInput) -> CityInput:
        """
        Update a city.

        Args:
            city (Type[City]): The city instance.
            data (CityInput): The updated city data.

        Returns:
            CityInput: The updated city data.
        """
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(city, key, value)
        self.session.commit()
        self.session.refresh(city)
        return CityInput(**city.__dict__)

    def delete(self, city: Type[City]) -> bool:
        """
        Delete a city.

        Args:
            city (Type[City]): The city instance.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        self.session.delete(city)
        self.session.commit()
        return True
