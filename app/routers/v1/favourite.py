from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from schemas.favourite import FavouriteInput
from services.favourite_service import FavouriteService

router = APIRouter(
    prefix="/favourite",
    tags=["favourite"]
)


@router.post("", status_code=201, response_model=FavouriteInput)
def create(favourite: FavouriteInput, session: Session = Depends(get_db)):
    _service = FavouriteService(session).create(favourite)
    return _service
