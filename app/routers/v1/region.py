from fastapi import APIRouter, Depends
from services.region_service import RegionService
from schemas.location import RegionOutput, RegionInput
from config.database import get_db
from sqlalchemy.orm import Session
from pydantic import UUID4


router = APIRouter(
    prefix="/region",
    tags=["region"]
)


@router.post("")
def create_region(data: RegionInput, session: Session = Depends(get_db)):
    _service = RegionService(session)
    return _service.create(data)


@router.get("")
def get_regions(session: Session = Depends(get_db)):
    _service = RegionService(session)
    return _service.get_all()


@router.delete("/{id}")
def delete_region(_id: UUID4, session: Session = Depends(get_db)):
    _service = RegionService(session)
    return _service.delete(_id)


@router.put("/{id}")
def update_region(_id: UUID4, data: RegionInput, session: Session = Depends(get_db)):
    _service = RegionService(session)
    return _service.update(_id, data)
