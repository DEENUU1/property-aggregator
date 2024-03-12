from .scrape_strategy import ScrapeStrategy


class Scraper:
    def __init__(self, scraping_strategy: ScrapeStrategy):
        self.scraping_strategy = scraping_strategy

    def scrape(self):
        return self.scraping_strategy.scrape()
