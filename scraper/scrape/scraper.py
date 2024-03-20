from .scrape_strategy import ScrapeStrategy


class Scraper:
    """
    Scraper class for performing scraping based on a provided scraping strategy.

    Attributes:
        scraping_strategy (ScrapeStrategy): An instance of ScrapeStrategy representing the scraping strategy.
    """

    def __init__(self, scraping_strategy: ScrapeStrategy):
        """
        Initialize the Scraper with a given scraping strategy.

        Args:
            scraping_strategy (ScrapeStrategy): An instance of ScrapeStrategy representing the scraping strategy.
        """
        self.scraping_strategy = scraping_strategy

    def scrape(self):
        """
        Perform scraping based on the provided scraping strategy.

        Returns:
            None
        """
        return self.scraping_strategy.scrape()
