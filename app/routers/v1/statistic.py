from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.auth import get_current_user
from config.database import get_db
from schemas.user import UserInDB
from services.statistics.offer_statistic_service import OfferStatisticService
from services.statistics.user_statistic_service import UserStatisticService

router = APIRouter(
    prefix="/statistic",
    tags=["statistic"]
)


@router.get("/offer/timeline")
def get_offer_timeline(
        db: Session = Depends(get_db),
        current_user: UserInDB = Depends(get_current_user)
):
    """
    Retrieve offer statistics over time.

    Args:
        db (Session): Database session.
        current_user (UserInDB): Current user's details.

    Returns:
        Statistics: Offer statistics over time.
    """
    _service = OfferStatisticService(db)
    return _service.get_number_of_offers_by_month(current_user.id)


@router.get("/offer/category")
def get_offer_count_by_category(
        db: Session = Depends(get_db),
        current_user: UserInDB = Depends(get_current_user)
):
    """
    Retrieve offer count grouped by category.

    Args:
        db (Session): Database session.
        current_user (UserInDB): Current user's details.

    Returns:
        Statistics: Offer count grouped by category.
    """
    _service = OfferStatisticService(db)
    return _service.count_offers_by_category(current_user.id)


@router.get("/offer/subcategory")
def get_offer_count_by_subcategory(
        db: Session = Depends(get_db),
        current_user: UserInDB = Depends(get_current_user)
):
    """
    Retrieve offer count grouped by subcategory.

    Args:
        db (Session): Database session.
        current_user (UserInDB): Current user's details.

    Returns:
        Statistics: Offer count grouped by subcategory.
    """
    _service = OfferStatisticService(db)
    return _service.count_offers_by_subcategory(current_user.id)


@router.get("/user/timeline")
def get_user_timeline(
        db: Session = Depends(get_db),
        current_user: UserInDB = Depends(get_current_user)
):
    """
    Retrieve user statistics over time.

    Args:
        db (Session): Database session.
        current_user (UserInDB): Current user's details.

    Returns:
        Statistics: User statistics over time.
    """
    _service = UserStatisticService(db)
    return _service.get_number_of_users_by_month(current_user.id)
