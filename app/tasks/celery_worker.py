from celery import Celery
from celery.schedules import crontab
from sqlalchemy.orm import Session

from config.settings import settings
from notification.context import Context
from notification.email_notification import EmailNotificationStrategy
from schemas.notification import NotificationInput
from services.notification_service import NotificationService
from services.notificationfilter_service import NotificationFilterService
from services.offer_service import OfferService

celery_app = Celery(
    'tasks',
    broker=settings.BROKER,
    backend=settings.BACKEND
)

celery_app.conf.beat_schedule = {
    "create_notification": {
        "task": "create_notifications",
        "schedule": crontab(minute="0", hour="0")
    }
}


@celery_app.task(name="create_notifications")
def create_notifications(db: Session) -> None:
    """
    Celery task to create notifications for users based on their notification filters.

    Args:
        db (Session): Database session.
    """
    notification_filters = NotificationFilterService(db).get_all_active()

    for notification_filter in notification_filters:
        if notification_filter.user_id is None:
            continue

        offers = OfferService(db).get_all(
            offset=1,
            page_size=100,
            category=notification_filter.category,
            sub_category=notification_filter.sub_category,
            building_type=notification_filter.building_type,
            price_min=notification_filter.price_min,
            price_max=notification_filter.price_max,
            area_min=notification_filter.area_min,
            area_max=notification_filter.area_max,
            rooms=notification_filter.rooms,
            furniture=notification_filter.furniture,
            floor=notification_filter.floor,
            query=notification_filter.query,
        )

        notification_input = NotificationInput(
            user_id=notification_filter.user_id,
            title=f"New offers for {notification_filter.category}",
            message=f"There are {len(offers.offers)} offers for {notification_filter.category}",
        )

        notification_service = NotificationService(db)
        notification_object = notification_service.create(notification_input)

        offers_ids = [offer.get("id") for offer in offers.offers]
        notification_service.update_offers(notification_object.id, offers_ids)

        context = Context(EmailNotificationStrategy())
        context.send_notification(notification_object)
