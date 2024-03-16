from typing import List, Type

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from models.notification import Notification
from models.offer import Offer
from repositories.notification_repository import NotificationRepository
from schemas.notification import NotificationOutput, NotificationInput


class NotificationService:
    def __init__(self, session: Session):
        self.repository = NotificationRepository(session)

    def create(self, notification: NotificationInput) -> NotificationOutput:
        return self.repository.create(notification)

    def get_all_by_user(self, user_id) -> List[NotificationOutput]:
        return self.repository.get_all_by_user_id(user_id)

    def mark_as_read(self, _id: UUID4) -> bool:
        if not self.repository.notification_exists_by_id(_id):
            HTTPException(status_code=404, detail="Notification not found")

        notification = self.repository.get_notification(_id)
        self.repository.mark_as_read(notification)
        return True

    def get_notification_by_id(self, _id: UUID4) -> NotificationOutput:
        if not self.repository.notification_exists_by_id(_id):
            HTTPException(status_code=404, detail="Notification not found")

        return self.repository.get_by_id(_id)

    def update_offers(self, notification: Type[Notification], offers: List[Type[Offer]]) -> bool:
        return self.repository.update_offers(notification, offers)
