from data.site import Site
from scrape import olx_scraper, scraper, otodom_scraper


def run_scrape(site: Site) -> None:
    """
    Run scraping for the specified site.

    Args:
        site (Site): The site to scrape.

    Returns:
        None
    """
    if site == Site.OLX:
        site_scraper = olx_scraper.OlxScraper()
    elif site == Site.OTODOM:
        site_scraper = otodom_scraper.OtodomScraper()
    else:
        raise ValueError(f"Unknown site: {site}")

    scraper.Scraper(site_scraper).scrape()
