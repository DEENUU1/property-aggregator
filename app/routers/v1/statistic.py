from config.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from repositories.statistics.offer_statistic_repository import OfferStatisticRepository


router = APIRouter(
    prefix="/statistic",
    tags=["statistic"]
)


@router.get("/offer/timeline")
def get_offer_timeline(db: Session = Depends(get_db)):
    return OfferStatisticRepository(db).get_number_of_offers_by_month()

