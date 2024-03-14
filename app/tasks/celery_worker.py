from celery import Celery
from config.settings import settings

celery_app = Celery(
    'tasks',
    broker=settings.BROKER,
    backend=settings.BACKEND
)
