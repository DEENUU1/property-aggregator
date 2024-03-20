from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from auth.auth import get_current_user
from config.database import get_db
from schemas.favourite import FavouriteInput, FavouriteOfferOutput
from schemas.user import UserInDB
from services.favourite_service import FavouriteService

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
    """
    Create a new favourite.

    Args:
        favourite (FavouriteInput): Favourite data to be created.
        session (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (UserInDB, optional): Current user. Defaults to Depends(get_current_user).

    Returns:
        FavouriteInput: Created favourite data.
    """
    favourite.user_id = current_user.id
    _service = FavouriteService(session).create(favourite)
    return _service


@router.delete("/{_id}", status_code=204)
def delete(
        _id: UUID4,
        session: Session = Depends(get_db),
        current_user: UserInDB = Depends(get_current_user),
):
    """
    Delete a favourite by ID.

    Args:
        _id (UUID4): ID of the favourite to delete.
        session (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (UserInDB, optional): Current user. Defaults to Depends(get_current_user).

    Returns:
        None
    """
    _service = FavouriteService(session).delete(_id, current_user.id)
    if not _service:
        raise HTTPException(status_code=404, detail="Favourite not found")


@router.get("", status_code=200, response_model=List[FavouriteOfferOutput])
def get_all_by_user(
        session: Session = Depends(get_db),
        current_user: UserInDB = Depends(get_current_user),
):
    """
    Get all favourites by user.

    Args:
        session (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (UserInDB, optional): Current user. Defaults to Depends(get_current_user).

    Returns:
        List[FavouriteOfferOutput]: List of favourites of the current user.
    """
    _service = FavouriteService(session).get_all_by_user(current_user.id)
    return _service
