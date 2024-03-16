from sqlalchemy.orm import Session
from schemas.notification import NotificationInput, NotificationOutput
from models.notification import Notification
from pydantic import UUID4
from typing import Type, List


class NotificationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: NotificationInput) -> NotificationOutput:
        notification = Notification(**data.model_dump(exclude_none=True))
        self.session.add(notification)
        self.session.commit()
        self.session.refresh(notification)
        return NotificationOutput(**notification.dict(), id=notification.id)

    def notification_exists_by_id(self, _id: UUID4) -> bool:
        notification = self.session.query(Notification).filter(Notification.id == _id).first()
        return notification is not None

    def update_status(self, notification: Type[Notification], status: bool) -> bool:
        notification.active = status
        self.session.commit()
        return True

    def get_notification_by_id(self, _id: UUID4) -> Type[Notification]:
        notification = self.session.query(Notification).filter(Notification.id == _id).first()
        return notification

    def get_all(self) -> List[NotificationOutput]:
        notifications = self.session.query().all()
        return [NotificationOutput(**notification) for notification in notifications]

    def get_all_by_user(self, user_id: UUID4) -> List[NotificationOutput]:
        notifications = self.session.query(Notification).filter(Notification.user_id == user_id).all()
        return [NotificationOutput(**notification) for notification in notifications]




