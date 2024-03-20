from typing import List

from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from auth.auth import get_current_user
from config.database import get_db
from schemas.notification import NotificationOutput
from schemas.notification_filter import (
    NotificationFilterInput,
    NotificationFilterOutput,
    NotificationFilterUpdateStatus
)
from schemas.user import UserInDB
from services.notification_service import NotificationService
from services.notificationfilter_service import NotificationFilterService

router = APIRouter(
    prefix="/notification",
    tags=["notification"]
)


@router.post("/filter", status_code=201, response_model=NotificationFilterOutput)
def create(notification: NotificationFilterInput, db: Session = Depends(get_db),
           current_user: UserInDB = Depends(get_current_user)):
    """
    Create a new notification filter for the current user.

    Args:
        notification (NotificationFilterInput): The notification filter details.
        db (Session): Database session.
        current_user (UserInDB): Current user's details.

    Returns:
        NotificationFilterOutput: Details of the created notification filter.
    """
    _service = NotificationFilterService(db)
    notification.user_id = current_user.id
    return _service.create(notification)


@router.put("/filter/{_id}", status_code=200)
def update_status(status: NotificationFilterUpdateStatus, _id: UUID4, db: Session = Depends(get_db),
                  current_user: UserInDB = Depends(get_current_user)):
    """
    Update the status of a notification filter.

    Args:
        status (NotificationFilterUpdateStatus): The status to be updated.
        _id (UUID4): The ID of the notification filter to be updated.
        db (Session): Database session.
        current_user (UserInDB): Current user's details.

    Returns:
        None
    """
    _service = NotificationFilterService(db)
    _service.update_status(_id, status.status, current_user.id)


@router.delete("/filter/{_id}", status_code=204)
def delete(_id: UUID4, db: Session = Depends(get_db),
           current_user: UUID4 = Depends(get_current_user)):
    """
    Delete a notification filter.

    Args:
        _id (UUID4): The ID of the notification filter to be deleted.
        db (Session): Database session.
        current_user (UUID4): Current user's ID.

    Returns:
        None
    """
    _service = NotificationFilterService(db)
    _service.delete(_id, current_user.id)


@router.get("/filter", status_code=200, response_model=List[NotificationFilterOutput])
def get_all_by_user(db: Session = Depends(get_db),
                    current_user: UserInDB = Depends(get_current_user)):
    """
    Retrieve all notification filters belonging to the current user.

    Args:
        db (Session): Database session.
        current_user (UserInDB): Current user's details.

    Returns:
        List[NotificationFilterOutput]: List of notification filters belonging to the current user.
    """
    _service = NotificationFilterService(db)
    return _service.get_all_by_user(current_user.id)


@router.get("", status_code=200, response_model=List[NotificationOutput])
def get_notifications_by_user(db: Session = Depends(get_db),
                              current_user: UserInDB = Depends(get_current_user)):
    """
    Retrieve all notifications belonging to the current user.

    Args:
        db (Session): Database session.
        current_user (UserInDB): Current user's details.

    Returns:
        List[NotificationOutput]: List of notifications belonging to the current user.
    """
    _service = NotificationService(db)
    return _service.get_all_by_user(current_user.id)


@router.get("/{_id}", status_code=200, response_model=NotificationOutput)
def get_notification_by_user(_id: UUID4, db: Session = Depends(get_db),
                             current_user: UserInDB = Depends(get_current_user)):
    """
    Retrieve a specific notification belonging to the current user.

    Args:
        _id (UUID4): The ID of the notification to be retrieved.
        db (Session): Database session.
        current_user (UserInDB): Current user's details.

    Returns:
        NotificationOutput: Details of the requested notification.
    """
    _service = NotificationService(db)
    return _service.get_notification_by_id(_id, current_user.id)


@router.get("/unread", status_code=200)
def get_unread_user_count(db: Session = Depends(get_db),
                          current_user: UserInDB = Depends(get_current_user)):
    """
    Retrieve the count of unread notifications for the current user.

    Args:
        db (Session): Database session.
        current_user (UserInDB): Current user's details.

    Returns:
        int: Count of unread notifications for the current user.
    """
    _service = NotificationService(db)
    return _service.get_unread_user_count(current_user.id)
