from schemas.notification import NotificationOutput
from .abc import notification_strategy


class EmailNotificationStrategy(notification_strategy.NotificationStrategy):
    """
    Notification strategy for sending email notifications.
    """

    def notify(self, data: NotificationOutput) -> None:
        """
        Send an email notification.

        Args:
            data (NotificationOutput): The notification data.
        """
        print(f"Sending email notification: {data.message} to {data.user_id}")
        return
