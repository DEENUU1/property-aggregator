from fastapi import APIRouter, Depends, Query
from pydantic import UUID4
from sqlalchemy.orm import Session

from config.database import get_db
from schemas.offer import OfferInput, OfferScraper
from services.offer_service import OfferService
from enums.offer_sort import OfferSortEnum

router = APIRouter(
    prefix="/offer",
    tags=["offer"]
)


@router.post("", status_code=201, response_model=OfferInput)
def create(offers: OfferInput, session: Session = Depends(get_db)):
    _service = OfferService(session).create(offers)
    return _service


@router.post("/scraper", status_code=201)
def create_scraper(offer: OfferScraper, session: Session = Depends(get_db)):
    _service = OfferService(session).create_scraper(offer)
    return _service


@router.delete("/{_id}", status_code=204)
def delete(_id: UUID4, session: Session = Depends(get_db)):
    _service = OfferService(session).delete(_id)
    return _service


@router.get("", status_code=200)
def get_all(
        session: Session = Depends(get_db),
        page: int = Query(1, gt=0),
        page_size: int = Query(15, qt=0),
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
        # TODO add filter by city and region
):
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
def get_details(_id: UUID4, session: Session = Depends(get_db)):
    _service = OfferService(session).get_by_id(_id)
    return _service
