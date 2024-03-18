from typing import List, Type

from pydantic import UUID4
from sqlalchemy.orm import Session

from models.notification import Notification
from models.offer import Offer
from schemas.notification import NotificationOutput, NotificationInput


class NotificationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, notification: NotificationInput) -> NotificationOutput:
        new_notification = Notification(**notification.model_dump(exclude_none=True))
        self.session.add(new_notification)
        self.session.commit()
        self.session.refresh(new_notification)
        return NotificationOutput(**new_notification.__dict__)

    def get_all_by_user_id(self, user_id: UUID4) -> List[NotificationOutput]:
        notifications = self.session.query(Notification).filter(Notification.user_id == user_id).all()
        return [
            NotificationOutput(**notification.__dict__) for notification in notifications
        ]

    def get_by_id(self, _id: UUID4) -> NotificationOutput:
        notification = self.session.query(Notification).filter(Notification.id == _id).first()
        return NotificationOutput(**notification.__dict__)

    def notification_exists_by_id(self, _id: UUID4) -> bool:
        notification = self.session.query(Notification).filter(Notification.id == _id).first()
        if notification:
            return True
        else:
            return False

    def get_notification(self, _id: UUID4) -> Type[Notification]:
        notification = self.session.query(Notification).filter(Notification.id == _id).first()
        return notification

    def mark_as_read(self, notification: Type[Notification]) -> bool:
        notification.read = True
        self.session.commit()
        self.session.refresh(notification)
        return True

    def get_notification_by_id(self, _id: UUID4) -> NotificationOutput:
        notification = self.session.query(Notification).filter(Notification.id == _id).first()
        return NotificationOutput(**notification.model_dump(exclude_none=True))

    def update_offers(self, notification: Type[Notification], offers: List[Type[Offer]]) -> bool:
        for offer in offers:
            if offer not in notification.offers:
                notification.offers.append(offer)
        self.session.commit()

        print(notification.offers)
        return True

    def get_unread_user_count(self, user_id: UUID4) -> int:
        return (self.session.query(Notification).filter(
            Notification.user_id == user_id, Notification.read == False).count())
