class ScrapeStrategy:
    """
    Base class for defining scraping strategies.

    Methods:
        scrape(self) -> None: Abstract method to be implemented by subclasses for actual scraping.
    """

    def scrape(self) -> None:
        """
        Abstract method for scraping data.

        This method should be implemented by subclasses to define specific scraping strategies.
        """
        raise NotImplementedError("Subclasses must implement the scrape method.")
