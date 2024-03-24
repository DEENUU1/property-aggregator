from fastapi import APIRouter, Depends, Query
from pydantic import UUID4
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from auth.auth import get_current_user
from config.database import get_db
from enums.offer_sort import OfferSortEnum
from schemas.offer import OfferScraper, OfferList
from schemas.user import UserIn
from services.offer_service import OfferService

router = APIRouter(
    prefix="/offer",
    tags=["offer"]
)


@router.post("", status_code=201)
def create(offer: List[OfferScraper], session: Session = Depends(get_db)):
    """
    Create a new offers.

    Args:
        offer (OfferScraper): Details of the offer to be created.
        session (Session): Database session.

    Returns:
        List[OfferScraper]: Details of the created offers.
    """
    _service = OfferService(session).create(offer)
    return _service


@router.delete("/{_id}", status_code=204)
def delete(_id: UUID4, session: Session = Depends(get_db),
           current_user: UserIn = Depends(get_current_user)):
    """
    Delete an offer.

    Args:
        _id (UUID4): The ID of the offer to be deleted.
        session (Session): Database session.
        current_user (UserIn): Current user's details.

    Returns:
        None
    """
    _service = OfferService(session).delete(_id, current_user.id)
    return _service


@router.get("", status_code=200)
def get_all(
        session: Session = Depends(get_db),
        page: int = Query(1, gt=0),
        page_size: int = Query(15, gt=0),
        category: str = Query(None),
        sub_category: str = Query(None),
        building_type: str = Query(None),
        price_min: int = Query(None, gt=0),
        price_max: int = Query(None, gt=0),
        area_min: int = Query(None, gt=0),
        area_max: int = Query(None, gt=0),
        rooms: int = Query(None, gt=0),
        furniture: bool = Query(None),
        floor: int = Query(None),
        query: str = Query(None),
        sort_by: OfferSortEnum = Query(OfferSortEnum.NEWEST)
):
    """
    Retrieve all offers based on the provided filters and sorting criteria.

    Args:
        session (Session): Database session.
        page (int): Page number for pagination (default is 1).
        page_size (int): Number of offers per page (default is 15).
        category (str): Category filter.
        sub_category (str): Sub-category filter.
        building_type (str): Building type filter.
        price_min (int): Minimum price filter.
        price_max (int): Maximum price filter.
        area_min (int): Minimum area filter.
        area_max (int): Maximum area filter.
        rooms (int): Number of rooms filter.
        furniture (bool): Furniture filter.
        floor (int): Floor filter.
        query (str): Search query.
        sort_by (OfferSortEnum): Sorting criteria (default is NEWEST).

    Returns:
        List[OfferScraper]: List of offers based on the provided filters and sorting criteria.
    """
    _service = OfferService(session).get_all(
        offset=page,
        page_size=page_size,
        category=category,
        sub_category=sub_category,
        building_type=building_type,
        price_min=price_min,
        price_max=price_max,
        area_min=area_min,
        area_max=area_max,
        rooms=rooms,
        furniture=furniture,
        floor=floor,
        query=query,
        sort_by=sort_by,
    )
    return _service


@router.get("/{_id}", status_code=200)
def get_details(_id: UUID4, session: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Retrieve details of a specific offer.

    Args:
        _id (UUID4): The ID of the offer to retrieve details for.
        session (Session): Database session.

    Returns:
        OfferScraper: Details of the requested offer.
    """
    _service = OfferService(session).get_by_id(_id)
    return _service
