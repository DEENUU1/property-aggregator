from .parse_strategy import ParseStrategy


class Parser:
    """A class for parsing data using a specified parse strategy.

    This class takes a parse strategy as input and utilizes it to parse data.

    Attributes:
        __parser_strategy (ParseStrategy): The strategy used for parsing data.

    Methods:
        parse(data, *args, **kwargs): Parses the data using the specified strategy.
    """

    def __init__(self, parser_strategy: ParseStrategy):
        """Initialize the Parser with a parse strategy.

        Args:
            parser_strategy (ParseStrategy): The strategy used for parsing data.
        """
        self.__parser_strategy = parser_strategy

    def parse(self, data, *args, **kwargs):
        """Parse the data using the specified strategy.

        Args:
            data: The data to be parsed.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The parsed data.
        """
        return self.__parser_strategy.parse(data, *args, **kwargs)
