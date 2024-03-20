from typing import Type, List

from pydantic import UUID4
from sqlalchemy.orm import Session

from models.notification_filter import NotificationFilter
from schemas.notification_filter import NotificationFilterInput, NotificationFilterOutput


class NotificationFilterRepository:
    """
    Repository class for handling notification filters.
    """

    def __init__(self, session: Session):
        """
        Initialize the repository with a database session.

        Args:
            session (Session): The database session.
        """
        self.session = session

    def create(self, data: NotificationFilterInput) -> NotificationFilterOutput:
        """
        Create a new notification filter.

        Args:
            data (NotificationFilterInput): The notification filter data.

        Returns:
            NotificationFilterOutput: The created notification filter.
        """
        notification = NotificationFilter(**data.model_dump(exclude_none=True))
        self.session.add(notification)
        self.session.commit()
        self.session.refresh(notification)
        return NotificationFilterOutput(**notification.__dict__)

    def notification_exists_by_id(self, _id: UUID4) -> bool:
        """
        Check if a notification filter exists by ID.

        Args:
            _id (UUID4): The notification filter ID.

        Returns:
            bool: True if the notification filter exists, False otherwise.
        """
        notification = self.session.query(NotificationFilter).filter(NotificationFilter.id == _id).first()
        return notification is not None

    def update_status(self, notification: Type[NotificationFilter], status: bool) -> bool:
        """
        Update the status of a notification filter.

        Args:
            notification (Type[NotificationFilter]): The notification filter instance.
            status (bool): The new status.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        notification.active = status
        self.session.commit()
        return True

    def get_notification_by_id(self, _id: UUID4) -> Type[NotificationFilter]:
        """
        Get a notification filter by ID.

        Args:
            _id (UUID4): The notification filter ID.

        Returns:
            Type[NotificationFilter]: The notification filter instance.
        """
        notification = self.session.query(NotificationFilter).filter(NotificationFilter.id == _id).first()
        return notification

    def get_all(self) -> List[NotificationFilterOutput]:
        """
        Get all notification filters.

        Returns:
            List[NotificationFilterOutput]: A list of notification filter outputs.
        """
        notifications = self.session.query().all()
        return [NotificationFilterOutput(**notification.__dict__) for notification in notifications]

    def get_all_active(self) -> List[NotificationFilterOutput]:
        """
        Get all active notification filters.

        Returns:
            List[NotificationFilterOutput]: A list of active notification filter outputs.
        """
        notifications = self.session.query(NotificationFilter).filter(NotificationFilter.active == True).all()
        return [NotificationFilterOutput(**notification.__dict__) for notification in notifications]

    def get_all_by_user(self, user_id: UUID4) -> List[NotificationFilterOutput]:
        """
        Get all notification filters by user ID.

        Args:
            user_id (UUID4): The user ID.

        Returns:
            List[NotificationFilterOutput]: A list of notification filter outputs.
        """
        notifications = self.session.query(NotificationFilter).filter(NotificationFilter.user_id == user_id).all()
        return [NotificationFilterOutput(**notification.__dict__) for notification in notifications]

    def delete(self, notification: Type[NotificationFilter]) -> bool:
        """
        Delete a notification filter.

        Args:
            notification (Type[NotificationFilter]): The notification filter instance.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        self.session.delete(notification)
        self.session.commit()
        return True
