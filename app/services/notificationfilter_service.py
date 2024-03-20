from typing import List

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from repositories.notificationfilter_repository import NotificationFilterRepository
from schemas.notification_filter import NotificationFilterOutput, NotificationFilterInput
from services.user_service import UserService


class NotificationFilterService:
    """
    Service class for handling notification filters.
    """

    def __init__(self, session: Session):
        """
        Initialize the service.

        Args:
            session (Session): Database session.
        """
        self.repository = NotificationFilterRepository(session)
        self.user_service = UserService(session)

    def create(self, data: NotificationFilterInput) -> NotificationFilterOutput:
        """
        Create a new notification filter.

        Args:
            data (NotificationFilterInput): Details of the notification filter to be created.

        Returns:
            NotificationFilterOutput: Details of the created notification filter.
        """
        return self.repository.create(data)

    def update_status(self, _id: UUID4, status: bool, user_id: UUID4) -> bool:
        """
        Update the status of a notification filter.

        Args:
            _id (UUID4): ID of the notification filter.
            status (bool): New status of the notification filter.
            user_id (UUID4): ID of the user performing the action.

        Returns:
            bool: True if update is successful, False otherwise.
        """
        if not self.repository.notification_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Notification filter does not exist")

        notification = self.repository.get_notification_by_id(_id)

        if notification.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not allowed to update this notification filter")

        return self.repository.update_status(notification, status)

    def get_all(self) -> List[NotificationFilterOutput]:
        """
        Retrieve all notification filters.

        Returns:
            List[NotificationFilterOutput]: List of all notification filters.
        """
        return self.repository.get_all()

    def get_all_active(self) -> List[NotificationFilterOutput]:
        """
        Retrieve all active notification filters.

        Returns:
            List[NotificationFilterOutput]: List of all active notification filters.
        """
        return self.repository.get_all_active()

    def get_all_by_user(self, user_id: UUID4) -> List[NotificationFilterOutput]:
        """
        Retrieve all notification filters of a user.

        Args:
            user_id (UUID4): ID of the user.

        Returns:
            List[NotificationFilterOutput]: List of notification filters of the user.
        """
        return self.repository.get_all_by_user(user_id)

    def delete(self, _id: UUID4, user_id: UUID4) -> bool:
        """
        Delete a notification filter.

        Args:
            _id (UUID4): ID of the notification filter to be deleted.
            user_id (UUID4): ID of the user performing the action.

        Returns:
            bool: True if deletion is successful, False otherwise.
        """
        if not self.repository.notification_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Notification filter does not exist")
        notification = self.repository.get_notification_by_id(_id)

        if notification.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not allowed to delete this notification filter")

        return self.repository.delete(notification)
