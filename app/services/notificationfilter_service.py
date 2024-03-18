from repositories.notificationfilter_repository import NotificationFilterRepository
from schemas.notification_filter import NotificationFilterOutput, NotificationFilterInput
from sqlalchemy.orm import Session
from fastapi import HTTPException
from pydantic import UUID4
from typing import List


class NotificationFilterService:
    def __init__(self, session: Session):
        self.repository = NotificationFilterRepository(session)

    def create(self, data: NotificationFilterInput) -> NotificationFilterOutput:
        return self.repository.create(data)

    def update_status(self, _id: UUID4, status: bool) -> bool:
        if not self.repository.notification_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Notification filter does not exist")

        notification = self.repository.get_notification_by_id(_id)
        return self.repository.update_status(notification, status)

    def get_all(self) -> List[NotificationFilterOutput]:
        return self.repository.get_all()

    def get_all_active(self) -> List[NotificationFilterOutput]:
        return self.repository.get_all_active()

    def get_all_by_user(self, user_id: UUID4)-> List[NotificationFilterOutput]:
        return self.repository.get_all_by_user(user_id)

    def delete(self, _id: UUID4) -> bool:
        if not self.repository.notification_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Notification filter does not exist")
        notification = self.repository.get_notification_by_id(_id)
        return self.repository.delete(notification)

