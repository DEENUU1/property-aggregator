from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from tasks.celery_worker import create_notifications
from config.database import get_db

router = APIRouter(
    prefix="/health",
    tags=["root"]
)


@router.get("", status_code=200)
def health(session: Session = Depends(get_db)):
    """ Check if the service is running correctly """

    create_notifications(session)

    return {"status": "ok"}
