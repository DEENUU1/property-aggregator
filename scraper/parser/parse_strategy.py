from abc import ABC, abstractmethod


class ParseStrategy(ABC):
    """An abstract base class for defining parse strategies.

    This class defines the interface for parsing data using various strategies.
    Subclasses must implement the `parse` method.

    Attributes:
        None

    Methods:
        parse(data, *args, **kwargs): Abstract method to be implemented by subclasses
            for parsing data using a specific strategy.
    """

    @abstractmethod
    def parse(self, data, *args, **kwargs):
        """Parse method to be implemented by subclasses.

        Args:
            data: The data to be parsed.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The parsed data.
        """
        pass

