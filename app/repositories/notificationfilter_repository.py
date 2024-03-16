from typing import Type, List

from pydantic import UUID4
from sqlalchemy.orm import Session

from models.notification_filter import NotificationFilter
from schemas.notification_filter import NotificationFilterInput, NotificationFilterOutput


class NotificationFilterRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: NotificationFilterInput) -> NotificationFilterOutput:
        notification = NotificationFilter(**data.model_dump(exclude_none=True))
        self.session.add(notification)
        self.session.commit()
        self.session.refresh(notification)
        return NotificationFilterOutput(**notification.__dict__)

    def notification_exists_by_id(self, _id: UUID4) -> bool:
        notification = self.session.query(NotificationFilter).filter(NotificationFilter.id == _id).first()
        return notification is not None

    def update_status(self, notification: Type[NotificationFilter], status: bool) -> bool:
        notification.active = status
        self.session.commit()
        return True

    def get_notification_by_id(self, _id: UUID4) -> Type[NotificationFilter]:
        notification = self.session.query(NotificationFilter).filter(NotificationFilter.id == _id).first()
        return notification

    def get_all(self) -> List[NotificationFilterOutput]:
        notifications = self.session.query().all()
        return [NotificationFilterOutput(**notification.__dict__) for notification in notifications]

    def get_all_active(self) -> List[NotificationFilterOutput]:
        notifications = self.session.query(NotificationFilter).filter(NotificationFilter.active == True).all()
        return [NotificationFilterOutput(**notification.__dict__) for notification in notifications]

    def get_all_by_user(self, user_id: UUID4) -> List[NotificationFilterOutput]:
        notifications = self.session.query(NotificationFilter).filter(NotificationFilter.user_id == user_id).all()
        return [NotificationFilterOutput(**notification.__dict__) for notification in notifications]

    def delete(self, notification: Type[NotificationFilter]) -> bool:
        self.session.delete(notification)
        self.session.commit()
        return True
