from fastapi import APIRouter, Depends
from services.city_service import CityService
from schemas.location import CityInput, CityOutput
from config.database import get_db
from sqlalchemy.orm import Session
from pydantic import UUID4
from typing import List


router = APIRouter(
    prefix="/location/city",
    tags=["location"]
)


@router.post("", status_code=201, response_model=CityInput)
def create_city(data: CityInput, session: Session = Depends(get_db)):
    _service = CityService(session)
    return _service.create(data)


@router.get("/region/{region_id}", status_code=200, response_model=List[CityOutput])
def get_cities_by_region(region_id: UUID4, session: Session = Depends(get_db)):
    _service = CityService(session)
    return _service.get_all_by_region(region_id)


@router.get("", status_code=200, response_model=List[CityOutput])
def get_cities(session: Session = Depends(get_db)):
    _service = CityService(session)
    return _service.get_all()


@router.delete("/{_id}", status_code=204)
def delete_city(_id: UUID4, session: Session = Depends(get_db)):
    _service = CityService(session)
    return _service.delete(_id)


@router.put("/{_id}", status_code=200, response_model=CityInput)
def update_city(_id: UUID4, data: CityInput, session: Session = Depends(get_db)):
    _service = CityService(session)
    return _service.update(_id, data)
