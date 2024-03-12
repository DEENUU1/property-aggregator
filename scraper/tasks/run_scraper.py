from data.site import Site
from scrape import olx_scraper, scraper, otodom_scraper


def run_scrape(site: Site) -> None:
    if site == site.OLX:
        site_scraper = olx_scraper.OlxScraper()
    elif site == site.OTODOM:
        site_scraper = otodom_scraper.OtodomScraper()
    else:
        raise ValueError(f"Unknown site: {site}")

    scraper.Scraper(site_scraper).scrape()
