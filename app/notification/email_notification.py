from .abc import notification_strategy
from schemas.notification import NotificationOutput


class EmailNotificationStrategy(notification_strategy.NotificationStrategy):
    def notify(self, data: NotificationOutput) -> None:
        print(f"Sending email notification: {data.message} to {data.user_id}")
        return

