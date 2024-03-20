from typing import List

from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from auth.auth import get_current_user
from config.database import get_db
from schemas.location import RegionOutput, RegionInput
from schemas.user import UserIn
from services.region_service import RegionService

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
    """
    Create a new region.

    Args:
        data (RegionInput): Details of the region to be created.
        session (Session): Database session.
        current_user (UserIn): Current user's details.

    Returns:
        RegionOutput: Details of the created region.
    """
    _service = RegionService(session)
    return _service.create(data, current_user.id)


@router.get("", status_code=200, response_model=List[RegionOutput])
def get_regions(session: Session = Depends(get_db)) -> List[RegionOutput]:
    """
    Retrieve all regions.

    Args:
        session (Session): Database session.

    Returns:
        List[RegionOutput]: List of all regions.
    """
    _service = RegionService(session)
    return _service.get_all()


@router.delete("/{_id}", status_code=204)
def delete_region(
        _id: UUID4,
        session: Session = Depends(get_db),
        current_user: UserIn = Depends(get_current_user)
):
    """
    Delete a region.

    Args:
        _id (UUID4): The ID of the region to be deleted.
        session (Session): Database session.
        current_user (UserIn): Current user's details.

    Returns:
        None
    """
    _service = RegionService(session)
    return _service.delete(_id, current_user.id)


@router.put("/{_id}", status_code=200, response_model=RegionInput)
def update_region(
        _id: UUID4,
        data: RegionInput,
        session: Session = Depends(get_db),
        current_user: UserIn = Depends(get_current_user)
):
    """
    Update a region.

    Args:
        _id (UUID4): The ID of the region to be updated.
        data (RegionInput): Updated details of the region.
        session (Session): Database session.
        current_user (UserIn): Current user's details.

    Returns:
        RegionInput: Updated details of the region.
    """
    _service = RegionService(session)
    return _service.update(_id, data, current_user.id)
