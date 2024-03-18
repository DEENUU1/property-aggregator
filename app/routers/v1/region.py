from fastapi import APIRouter, Depends
from services.region_service import RegionService
from schemas.location import RegionOutput, RegionInput
from config.database import get_db
from sqlalchemy.orm import Session
from pydantic import UUID4
from schemas.user import UserIn
from auth.auth import get_current_user
from typing import List


router = APIRouter(
    prefix="/location/region",
    tags=["location"]
)


@router.post("", status_code=201, response_model=RegionOutput)
def create_region(
        data: RegionInput,
        session: Session = Depends(get_db),
        current_user: UserIn = Depends(get_current_user)
):
    _service = RegionService(session)
    return _service.create(data, current_user.id)


@router.get("", status_code=200, response_model=List[RegionOutput])
def get_regions(session: Session = Depends(get_db)):
    _service = RegionService(session)
    return _service.get_all()


@router.delete("/{_id}", status_code=204)
def delete_region(
        _id: UUID4,
        session: Session = Depends(get_db),
        current_user: UserIn = Depends(get_current_user)
):
    _service = RegionService(session)
    return _service.delete(_id, current_user.id)


@router.put("/{_id}", status_code=200, response_model=RegionInput)
def update_region(
        _id: UUID4,
        data: RegionInput,
        session: Session = Depends(get_db),
        current_user: UserIn = Depends(get_current_user)
):
    _service = RegionService(session)
    return _service.update(_id, data, current_user.id)
