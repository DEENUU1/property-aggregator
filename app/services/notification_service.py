from typing import List, Optional

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from repositories.notification_repository import NotificationRepository
from repositories.offer_repository import OfferRepository
from schemas.notification import NotificationOutput, NotificationInput


class NotificationService:
    def __init__(self, session: Session):
        self.repository = NotificationRepository(session)
        self.offer_repository = OfferRepository(session)

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

        notification = self.repository.get_notification(_id)
        self.repository.mark_as_read(notification)

        notification = self.repository.get_by_id(_id)
        return notification

    def update_offers(self, notification_id: UUID4, offers_id: List[Optional[UUID4]]) -> bool:
        if not self.repository.notification_exists_by_id(notification_id):
            HTTPException(status_code=404, detail="Notification not found")

        notification = self.repository.get_notification(notification_id)

        offers = []
        for _id in offers_id:
            if _id is not None:
                offer = self.offer_repository.get_offer_by_id(_id)
                offers.append(offer)

        return self.repository.update_offers(notification, offers)

    def get_unread_user_count(self, user_id: UUID4) -> int:
        return self.repository.get_unread_user_count(user_id)
