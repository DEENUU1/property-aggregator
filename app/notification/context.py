from .abc.notification_strategy import NotificationStrategy
from schemas.notification import NotificationOutput


class Context:
    def __init__(self, strategy: NotificationStrategy):
        self._strategy = strategy

    def send_notification(self, data: NotificationOutput):
        return self._strategy.notify(data)
