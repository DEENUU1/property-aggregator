from typing import List

from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from auth.auth import get_current_user
from config.database import get_db
from schemas.notification_filter import (
    NotificationFilterInput,
    NotificationFilterOutput,
    NotificationFilterUpdateStatus
)
from schemas.user import UserInDB
from services.notificationfilter_service import NotificationFilterService

router = APIRouter(
    prefix="/notification",
    tags=["notif"]
)


@router.post("/filter", status_code=201, response_model=NotificationFilterOutput)
def create(
        notification: NotificationFilterInput,
        db: Session = Depends(get_db),
        current_user: UserInDB = Depends(get_current_user)
):
    _service = NotificationFilterService(db)
    notification.user_id = current_user.id
    return _service.create(notification)


@router.put("/filter/{_id}", status_code=200)
def update_status(
        status: NotificationFilterUpdateStatus,
        _id: UUID4,
        db: Session = Depends(get_db),
        current_user: UserInDB = Depends(get_current_user)
):
    _service = NotificationFilterService(db)
    return _service.update_status(_id, status.status)


@router.delete("/filter/{_id}", status_code=204)
def delete(
        _id: UUID4,
        db: Session = Depends(get_db),
        current_user: UUID4 = Depends(get_current_user)
):
    _service = NotificationFilterService(db)
    return _service.delete(_id)


@router.get("/filter", status_code=200, response_model=List[NotificationFilterOutput])
def get_all_by_user(
        db: Session = Depends(get_db),
        current_user: UserInDB = Depends(get_current_user)
):
    _service = NotificationFilterService(db)
    return _service.get_all_by_user(current_user.id)
