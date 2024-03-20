from typing import List, Optional

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from repositories.notification_repository import NotificationRepository
from repositories.offer_repository import OfferRepository
from schemas.notification import NotificationOutput, NotificationInput


class NotificationService:
    """
    Service class for handling notifications.
    """

    def __init__(self, session: Session):
        """
        Initialize the service.

        Args:
            session (Session): Database session.
        """
        self.repository = NotificationRepository(session)
        self.offer_repository = OfferRepository(session)

    def create(self, notification: NotificationInput) -> NotificationOutput:
        """
        Create a new notification.

        Args:
            notification (NotificationInput): Details of the notification to be created.

        Returns:
            NotificationOutput: Details of the created notification.
        """
        return self.repository.create(notification)

    def get_all_by_user(self, user_id: UUID4) -> List[NotificationOutput]:
        """
        Retrieve all notifications of a user.

        Args:
            user_id (UUID4): ID of the user.

        Returns:
            List[NotificationOutput]: List of notifications of the user.
        """
        return self.repository.get_all_by_user_id(user_id)

    def get_notification_by_id(self, _id: UUID4, user_id: UUID4) -> NotificationOutput:
        """
        Retrieve a notification by ID.

        Args:
            _id (UUID4): ID of the notification.
            user_id (UUID4): ID of the user.

        Returns:
            NotificationOutput: Details of the retrieved notification.
        """
        if not self.repository.notification_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Notification not found")

        notification = self.repository.get_notification(_id)

        if notification.user_id != user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        self.repository.mark_as_read(notification)

        offer_list = []
        if notification.offers:
            for offer in notification.offers:
                offer_details = self.offer_repository.get_details(offer.id)
                offer_list.append(offer_details)

        result = NotificationOutput(
            id=notification.id,
            title=notification.title,
            message=notification.message,
            created_at=notification.created_at,
            read=notification.read,
            offers=offer_list,
            user_id=notification.user_id,
        )

        return result

    def update_offers(self, notification_id: UUID4, offers_id: List[Optional[UUID4]]) -> bool:
        """
        Update offers associated with a notification.

        Args:
            notification_id (UUID4): ID of the notification.
            offers_id (List[Optional[UUID4]]): List of offer IDs.

        Returns:
            bool: True if update is successful, False otherwise.
        """
        if not self.repository.notification_exists_by_id(notification_id):
            raise HTTPException(status_code=404, detail="Notification not found")

        notification = self.repository.get_notification(notification_id)
        offers = []
        for _id in offers_id:
            if _id is not None:
                offer = self.offer_repository.get_offer_by_id(_id)
                offers.append(offer)
        return self.repository.update_offers(notification, offers)

    def get_unread_user_count(self, user_id: UUID4) -> int:
        """
        Get the count of unread notifications for a user.

        Args:
            user_id (UUID4): ID of the user.

        Returns:
            int: Count of unread notifications.
        """
        return self.repository.get_unread_user_count(user_id)
