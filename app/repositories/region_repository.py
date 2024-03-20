from sqlalchemy.orm import Session
from models.location import Region
from schemas.location import RegionInput, RegionOutput
from typing import List, Optional, Type
from pydantic import UUID4

class RegionRepository:
    """
    Repository class for handling regions.
    """
    def __init__(self, session: Session):
        """
        Initialize the repository with a database session.

        Args:
            session (Session): The database session.
        """
        self.session = session

    def create(self, data: RegionInput) -> RegionOutput:
        """
        Create a new region.

        Args:
            data (RegionInput): The region data.

        Returns:
            RegionOutput: The created region.
        """
        region = Region(**data.model_dump(exclude_none=True))
        self.session.add(region)
        self.session.commit()
        self.session.refresh(region)
        return RegionOutput(id=region.id, name=region.name)

    def get_all(self) -> List[Optional[RegionOutput]]:
        """
        Get all regions.

        Returns:
            List[Optional[RegionOutput]]: List of regions.
        """
        regions = self.session.query(Region).all()
        return [RegionOutput(**region.__dict__) for region in regions]

    def get_region(self, _id: UUID4) -> RegionOutput:
        """
        Get a region by ID.

        Args:
            _id (UUID4): The ID of the region.

        Returns:
            RegionOutput: The region.
        """
        region = self.session.query(Region).filter_by(id=_id).first()
        return RegionOutput(**region.__dict__)

    def get_by_id(self, _id: UUID4) -> Type[Region]:
        """
        Get a region by ID.

        Args:
            _id (UUID4): The ID of the region.

        Returns:
            Type[Region]: The region instance.
        """
        return self.session.query(Region).filter_by(id=_id).first()

    def get_by_name(self, name: str) -> Type[Region]:
        """
        Get a region by name.

        Args:
            name (str): The name of the region.

        Returns:
            Type[Region]: The region instance.
        """
        return self.session.query(Region).filter_by(name=name).first()

    def region_exists_by_id(self, _id: UUID4) -> bool:
        """
        Check if a region exists by ID.

        Args:
            _id (UUID4): The ID of the region.

        Returns:
            bool: True if the region exists, False otherwise.
        """
        region = self.session.query(Region).filter_by(id=_id).first()
        return region is not None

    def region_exists_by_name(self, name: str) -> bool:
        """
        Check if a region exists by name.

        Args:
            name (str): The name of the region.

        Returns:
            bool: True if the region exists, False otherwise.
        """
        region = self.session.query(Region).filter_by(name=name).first()
        return region is not None

    def update(self, region: Type[Region], data: RegionInput) -> RegionInput:
        """
        Update a region.

        Args:
            region (Type[Region]): The region instance.
            data (RegionInput): The updated region data.

        Returns:
            RegionInput: The updated region data.
        """
        region.name = data.name
        self.session.commit()
        self.session.refresh(region)
        return RegionInput(**region.__dict__)

    def delete(self, region: Type[Region]) -> bool:
        """
        Delete a region.

        Args:
            region (Type[Region]): The region instance.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        self.session.delete(region)
        self.session.commit()
        return True
