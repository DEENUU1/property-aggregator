from typing import List

from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from config.database import get_db
from schemas.offer import OfferInput
from services.offer_service import OfferService

router = APIRouter(
    prefix="/offer",
    tags=["offer"]
)


@router.post("")
def create(offers: OfferInput, session: Session = Depends(get_db)):
    _service = OfferService(session).create(offers)
    return _service


@router.delete("/{_id}")
def delete(_id: UUID4, session: Session = Depends(get_db)):
    _service = OfferService(session).delete(_id)
    return _service


@router.get("")
def get_all(session: Session = Depends(get_db)):
    _service = OfferService(session).get_all()
    return _service


@router.get("/{_id}")
def get_details(_id: UUID4, session: Session = Depends(get_db)):
    _service = OfferService(session).get_by_id(_id)
    return _service
