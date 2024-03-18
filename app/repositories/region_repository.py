from sqlalchemy.orm import Session

from models.location import Region
from schemas.location import RegionInput, RegionOutput
from typing import List, Optional, Type
from pydantic import UUID4


class RegionRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, data: RegionInput) -> RegionOutput:
        region = Region(**data.model_dump(exclude_none=True))
        self.session.add(region)
        self.session.commit()
        self.session.refresh(region)
        return RegionOutput(id=region.id, name=region.name)

    def get_all(self) -> List[Optional[RegionOutput]]:
        regions = self.session.query(Region).all()
        return [RegionOutput(**region.__dict__) for region in regions]

    def get_region(self, _id: UUID4) -> RegionOutput:
        region = self.session.query(Region).filter_by(id=_id).first()
        return RegionOutput(**region.__dict__)

    def get_by_id(self, _id: UUID4) -> Type[Region]:
        return self.session.query(Region).filter_by(id=_id).first()

    def get_by_name(self, name: str) -> Type[Region]:
        return self.session.query(Region).filter_by(name=name).first()

    def region_exists_by_id(self, _id: UUID4) -> bool:
        region = self.session.query(Region).filter_by(id=_id).first()
        if region:
            return True
        return False

    def region_exists_by_name(self, name: str) -> bool:
        region = self.session.query(Region).filter_by(name=name).first()
        if region:
            return True
        return False

    def update(self, region: Type[Region], data: RegionInput) -> RegionInput:
        region.name = data.name
        self.session.commit()
        self.session.refresh(region)
        return RegionInput(**region.__dict__)

    def delete(self, region: Type[Region]) -> bool:
        self.session.delete(region)
        self.session.commit()
        return True

