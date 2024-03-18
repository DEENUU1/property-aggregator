from typing import List, Dict

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from repositories.statistics.user_statistic_repository import UserStatisticRepository
from services.user_service import UserService


class UserStatisticService:

    def __init__(self, session: Session):
        self.repository = UserStatisticRepository(session)
        self.user_service = UserService(session)

    def get_number_of_users_by_month(self, user_id: UUID4) -> List[Dict[str, int]]:
        if not self.user_service.is_superuser(user_id):
            raise HTTPException(status_code=403, detail="Forbidden")

        return self.repository.get_number_of_users_by_month()
