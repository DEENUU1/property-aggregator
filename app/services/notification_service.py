from repositories.notification_repository import NotificationRepository
from schemas.notification import NotificationOutput, NotificationInput
from sqlalchemy.orm import Session
from fastapi import HTTPException
from pydantic import UUID4
from typing import List


class NotificationService:
    def __init__(self, session: Session):
        self.repository = NotificationRepository(session)

    def create(self, data: NotificationInput) -> NotificationOutput:
        return self.repository.create(data)

    def update_status(self, _id: UUID4, status: bool) -> bool:
        if not self.repository.notification_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Notification does not exist")
        return self.repository.update_status(_id, status)

    def get_all(self) -> List[NotificationOutput]:
        return self.repository.get_all()

    def get_all_by_user(self, user_id: UUID4)-> List[NotificationOutput]:
        return self.repository.get_all_by_user(user_id)

    def delete(self, _id: UUID4) -> bool:
        if not self.repository.notification_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Notification does not exist")
        notification = self.repository.get_notification_by_id(_id)
        return self.repository.delete(notification)

