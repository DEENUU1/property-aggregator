from config.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from repositories.statistics.offer_statistic_repository import OfferStatisticRepository
from repositories.statistics.user_statistic_repository import UserStatisticRepository


router = APIRouter(
    prefix="/statistic",
    tags=["statistic"]
)


@router.get("/offer/timeline")
def get_offer_timeline(db: Session = Depends(get_db)):
    return OfferStatisticRepository(db).get_number_of_offers_by_month()


@router.get("offer/category")
def get_offer_count_by_category(db: Session = Depends(get_db)):
    return OfferStatisticRepository(db).count_offers_by_category()


@router.get("offer/subcategory")
def get_offer_count_by_subcategory(db: Session = Depends(get_db)):
    return OfferStatisticRepository(db).count_offers_by_subcategory()


@router.get("user/timeline")
def get_user_timeline(db: Session = Depends(get_db)):
    return UserStatisticRepository(db).get_number_of_userss_by_month()
