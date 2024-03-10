from fastapi import APIRouter, Depends
from services.city_service import CityService
from schemas.location import CityInput, CityOutput
from config.database import get_db
from sqlalchemy.orm import Session
from pydantic import UUID4


router = APIRouter(
    prefix="/location/city",
    tags=["location"]
)


@router.post("")
def create_city(data: CityInput, session: Session = Depends(get_db)):
    _service = CityService(session)
    return _service.create(data)


@router.get("")
def get_cities(session: Session = Depends(get_db)):
    _service = CityService(session)
    return _service.get_all()


@router.delete("/{_id}")
def delete_city(_id: UUID4, session: Session = Depends(get_db)):
    _service = CityService(session)
    return _service.delete(_id)
