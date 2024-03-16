from schemas.notification import NotificationOutput, NotificationInput
from models.notification import Notification
from sqlalchemy.orm import Session
from pydantic import UUID4
from typing import List, Type


class NotificationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, notification: NotificationInput) -> NotificationOutput:
        new_notification = Notification(**notification.model_dump(exclude_none=True))
        self.session.add(new_notification)
        self.session.commit()
        self.session.refresh(new_notification)
        return NotificationOutput(
            **new_notification.__dict__,
            id=new_notification.id,
            created_at=new_notification.created_at,
            read=new_notification.read,
        )

    def get_all_by_user_id(self, user_id: UUID4) -> List[NotificationOutput]:
        notifications = self.session.query(Notification).filter(Notification.user_id == user_id).all()
        return [
            NotificationOutput(**notification.model_dump(exclude_none=True)) for notification in notifications
        ]

    def get_by_id(self, _id: UUID4) -> NotificationOutput:
        notification = self.session.query(Notification).filter(Notification.id == id).first()
        return NotificationOutput(**notification.model_dump(exclude_none=True))

    def get_notification(self, _id: UUID4) -> Type[Notification]:
        notification = self.session.query(Notification).filter(Notification.id == id).first()
        return notification

    def mark_as_read(self, notification: Type[Notification]) -> bool:
        notification.read = True
        self.session.commit()
        self.session.refresh(notification)
        return True