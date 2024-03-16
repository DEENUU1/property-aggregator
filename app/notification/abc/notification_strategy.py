from abc import ABC, abstractmethod
from schemas.notification import NotificationOutput


class NotificationStrategy(ABC):
    @abstractmethod
    def notify(self, data: NotificationOutput):
        pass
