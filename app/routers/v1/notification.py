from typing import List

from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from auth.auth import get_current_user
from config.database import get_db
from schemas.notification import NotificationInput, NotificationOutput, NotificationUpdateStatus
from schemas.user import UserInDB
from services.notification_service import NotificationService

router = APIRouter(
    prefix="/notification",
    tags=["notification"]
)


@router.post("", status_code=201, response_model=NotificationOutput)
def create(
        notification: NotificationInput,
        db: Session = Depends(get_db),
        current_user: UserInDB = Depends(get_current_user)
):
    _service = NotificationService(db)
    notification.user_id = current_user.id
    return _service.create(notification)


@router.put("/{_id}", status_code=200)
def update_status(
        status: NotificationUpdateStatus,
        _id: UUID4,
        db: Session = Depends(get_db),
        current_user: UserInDB = Depends(get_current_user)
):
    _service = NotificationService(db)
    return _service.update_status(_id, status.status)


@router.delete("/{_id}", status_code=204)
def delete(
        _id: UUID4,
        db: Session = Depends(get_db),
        current_user: UUID4 = Depends(get_current_user)
):
    _service = NotificationService(db)
    return _service.delete(_id)


@router.get("", status_code=200, response_model=List[NotificationOutput])
def get_all_by_user(
        db: Session = Depends(get_db),
        current_user: UserInDB = Depends(get_current_user)
):
    _service = NotificationService(db)
    return _service.get_all_by_user(current_user.id)
