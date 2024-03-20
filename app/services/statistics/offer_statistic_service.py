from typing import List, Dict

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from repositories.statistics.offer_statistic_repository import OfferStatisticRepository
from services.user_service import UserService


class OfferStatisticService:
    """
    Service class for handling offer statistics.
    """

    def __init__(self, session: Session):
        """
        Initialize the service.

        Args:
            session (Session): Database session.
        """
        self.repository = OfferStatisticRepository(session)
        self.user_service = UserService(session)

    def get_number_of_offers_by_month(self, user_id: UUID4) -> List[Dict[str, int]]:
        """
        Get the number of offers per month.

        Args:
            user_id (UUID4): User ID.

        Returns:
            List[Dict[str, int]]: Number of offers per month.
        """
        if not self.user_service.is_superuser(user_id):
            raise HTTPException(status_code=403, detail="Forbidden")

        return self.repository.get_number_of_offers_by_month()

    def count_offers_by_category(self, user_id: UUID4) -> Dict[str, int]:
        """
        Count offers by category.

        Args:
            user_id (UUID4): User ID.

        Returns:
            Dict[str, int]: Number of offers by category.
        """
        if not self.user_service.is_superuser(user_id):
            raise HTTPException(status_code=403, detail="Forbidden")

        return self.repository.count_offers_by_category()

    def count_offers_by_subcategory(self, user_id: UUID4) -> Dict[str, int]:
        """
        Count offers by subcategory.

        Args:
            user_id (UUID4): User ID.

        Returns:
            Dict[str, int]: Number of offers by subcategory.
        """
        if not self.user_service.is_superuser(user_id):
            raise HTTPException(status_code=403, detail="Forbidden")

        return self.repository.count_offers_by_subcategory()
