from schemas.notification import NotificationOutput
from .abc.notification_strategy import NotificationStrategy


class Context:
    """
    Context class for handling notification strategies.
    """

    def __init__(self, strategy: NotificationStrategy):
        """
        Initialize the Context with a notification strategy.

        Args:
            strategy (NotificationStrategy): The notification strategy to use.
        """
        self._strategy = strategy

    def send_notification(self, data: NotificationOutput):
        """
        Send a notification using the selected strategy.

        Args:
            data (NotificationOutput): The notification data to send.
        """
        return self._strategy.notify(data)
