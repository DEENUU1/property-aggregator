from abc import ABC, abstractmethod

from schemas.notification import NotificationOutput


class NotificationStrategy(ABC):
    """
    Abstract base class for notification strategies.
    """

    @abstractmethod
    def notify(self, data: NotificationOutput):
        """
        Abstract method to notify based on the provided data.

        Args:
            data (NotificationOutput): The notification data.
        """
        pass
