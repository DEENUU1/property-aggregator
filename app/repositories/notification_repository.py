from typing import List, Type

from pydantic import UUID4
from sqlalchemy.orm import Session

from models.notification import Notification
from models.offer import Offer
from schemas.notification import NotificationOutput, NotificationInput


class NotificationRepository:
    """
    Repository class for handling notifications.
    """

    def __init__(self, session: Session):
        """
        Initialize the repository with a database session.

        Args:
            session (Session): The database session.
        """
        self.session = session

    def create(self, notification: NotificationInput) -> NotificationOutput:
        """
        Create a new notification.

        Args:
            notification (NotificationInput): The notification data.

        Returns:
            NotificationOutput: The created notification.
        """
        new_notification = Notification(**notification.model_dump(exclude_none=True))
        self.session.add(new_notification)
        self.session.commit()
        self.session.refresh(new_notification)
        return NotificationOutput(**new_notification.__dict__)

    def get_all_by_user_id(self, user_id: UUID4) -> List[NotificationOutput]:
        """
        Get all notifications by user ID.

        Args:
            user_id (UUID4): The user ID.

        Returns:
            List[NotificationOutput]: A list of notification outputs.
        """
        notifications = self.session.query(Notification).filter(Notification.user_id == user_id).all()
        return [
            NotificationOutput(**notification.__dict__) for notification in notifications
        ]

    def get_by_id(self, _id: UUID4) -> NotificationOutput:
        """
        Get a notification by ID.

        Args:
            _id (UUID4): The notification ID.

        Returns:
            NotificationOutput: The notification output.
        """
        notification = self.session.query(Notification).filter(Notification.id == _id).first()
        return NotificationOutput(**notification.__dict__)

    def notification_exists_by_id(self, _id: UUID4) -> bool:
        """
        Check if a notification exists by ID.

        Args:
            _id (UUID4): The notification ID.

        Returns:
            bool: True if the notification exists, False otherwise.
        """
        notification = self.session.query(Notification).filter(Notification.id == _id).first()
        return bool(notification)

    def get_notification(self, _id: UUID4) -> Type[Notification]:
        """
        Get a notification by ID.

        Args:
            _id (UUID4): The notification ID.

        Returns:
            Type[Notification]: The notification instance.
        """
        notification = self.session.query(Notification).filter(Notification.id == _id).first()
        return notification

    def mark_as_read(self, notification: Type[Notification]) -> bool:
        """
        Mark a notification as read.

        Args:
            notification (Type[Notification]): The notification instance.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        notification.read = True
        self.session.commit()
        self.session.refresh(notification)
        return True

    def get_notification_by_id(self, _id: UUID4) -> NotificationOutput:
        """
        Get a notification by ID.

        Args:
            _id (UUID4): The notification ID.

        Returns:
            NotificationOutput: The notification output.
        """
        notification = self.session.query(Notification).filter(Notification.id == _id).first()
        return NotificationOutput(**notification.model_dump(exclude_none=True))

    def update_offers(self, notification: Type[Notification], offers: List[Type[Offer]]) -> bool:
        """
        Update offers associated with a notification.

        Args:
            notification (Type[Notification]): The notification instance.
            offers (List[Type[Offer]]): The list of offer instances.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        for offer in offers:
            if offer not in notification.offers:
                notification.offers.append(offer)
        self.session.commit()
        return True

    def get_unread_user_count(self, user_id: UUID4) -> int:
        """
        Get the count of unread notifications for a user.

        Args:
            user_id (UUID4): The user ID.

        Returns:
            int: The count of unread notifications.
        """
        return self.session.query(Notification).filter(
            Notification.user_id == user_id, Notification.read == False
        ).count()
