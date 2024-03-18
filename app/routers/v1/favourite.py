from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from schemas.favourite import FavouriteInput, FavouriteOfferOutput
from services.favourite_service import FavouriteService
from schemas.user import UserInDB
from auth.auth import get_current_user
from pydantic import UUID4


router = APIRouter(
    prefix="/favourite",
    tags=["favourite"]
)


@router.post("", status_code=201, response_model=FavouriteInput)
def create(
        favourite: FavouriteInput,
        session: Session = Depends(get_db),
        current_user: UserInDB = Depends(get_current_user),
):
    favourite.user_id = current_user.id
    _service = FavouriteService(session).create(favourite)
    return _service


@router.delete("/{_id}", status_code=204)
def delete(
        _id: UUID4,
        session: Session = Depends(get_db),
        current_user: UserInDB = Depends(get_current_user),
):
    _service = FavouriteService(session).delete(_id)
    return _service


@router.get("", status_code=200, response_model=List[FavouriteOfferOutput])
def get_all_by_user(
        session: Session = Depends(get_db),
        current_user: UserInDB = Depends(get_current_user),
):
    _service = FavouriteService(session).get_all_by_user(current_user.id)
    return _service
