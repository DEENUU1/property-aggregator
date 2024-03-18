from typing import List, Dict

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from repositories.statistics.offer_statistic_repository import OfferStatisticRepository
from services.user_service import UserService


class OfferStatisticService:

    def __init__(self, session: Session):
        self.repository = OfferStatisticRepository(session)
        self.user_service = UserService(session)

    def get_number_of_offers_by_month(self, user_id: UUID4) -> List[Dict[str, int]]:
        if not self.user_service.is_superuser(user_id):
            raise HTTPException(status_code=403, detail="Forbidden")

        return self.repository.get_number_of_offers_by_month()

    def count_offers_by_category(self, user_id: UUID4) -> Dict[str, int]:
        if not self.user_service.is_superuser(user_id):
            raise HTTPException(status_code=403, detail="Forbidden")

        return self.repository.count_offers_by_category()

    def count_offers_by_subcategory(self, user_id: UUID4) -> Dict[str, int]:
        if not self.user_service.is_superuser(user_id):
            raise HTTPException(status_code=403, detail="Forbidden")

        return self.repository.count_offers_by_subcategory()
