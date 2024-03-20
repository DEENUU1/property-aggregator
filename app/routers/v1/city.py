from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from auth.auth import get_current_user
from config.database import get_db
from schemas.location import CityInput, CityOutput
from schemas.user import UserIn
from services.city_service import CityService

router = APIRouter(
    prefix="/location/city",
    tags=["location"]
)


@router.post("", status_code=201, response_model=CityOutput)
def create_city(
        data: CityInput, session: Session = Depends(get_db),
        current_user: UserIn = Depends(get_current_user)
):
    """
    Create a new city.

    Args:
        data (CityInput): City data to be created.
        session (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (UserIn, optional): Current user. Defaults to Depends(get_current_user).

    Returns:
        CityOutput: Created city.
    """
    _service = CityService(session)
    return _service.create(data, current_user.id)


@router.get("/region/{region_id}", status_code=200, response_model=List[CityOutput])
def get_cities_by_region(region_id: UUID4, session: Session = Depends(get_db)):
    """
    Get all cities by region ID.

    Args:
        region_id (UUID4): ID of the region.
        session (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        List[CityOutput]: List of cities in the specified region.
    """
    _service = CityService(session)
    return _service.get_all_by_region(region_id)


@router.get("", status_code=200, response_model=List[CityOutput])
def get_cities(session: Session = Depends(get_db)):
    """
    Get all cities.

    Args:
        session (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        List[CityOutput]: List of all cities.
    """
    _service = CityService(session)
    return _service.get_all()


@router.delete("/{_id}", status_code=204)
def delete_city(
        _id: UUID4,
        session: Session = Depends(get_db),
        current_user: UserIn = Depends(get_current_user)
):
    """
    Delete a city by ID.

    Args:
        _id (UUID4): ID of the city to delete.
        session (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (UserIn, optional): Current user. Defaults to Depends(get_current_user).

    Returns:
        None
    """
    _service = CityService(session)
    if not _service.delete(_id, current_user.id):
        raise HTTPException(status_code=404, detail="City not found")


@router.put("/{_id}", status_code=200, response_model=CityInput)
def update_city(
        _id: UUID4,
        data: CityInput,
        session: Session = Depends(get_db),
        current_user: UserIn = Depends(get_current_user)
):
    """
    Update a city by ID.

    Args:
        _id (UUID4): ID of the city to update.
        data (CityInput): Updated city data.
        session (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (UserIn, optional): Current user. Defaults to Depends(get_current_user).

    Returns:
        CityInput: Updated city data.
    """
    _service = CityService(session)
    city = _service.update(_id, data, current_user.id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city
