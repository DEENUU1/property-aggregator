from data.site import Site
from tasks import run_parser, run_scraper


def main() -> None:
    # run_scraper.run_scrape(Site.OTODOM)
    # run_scraper.run_scrape(Site.OLX)

    # run_parser.run_parser(Site.OTODOM)
    run_parser.run_parser(Site.OLX)


if __name__ == '__main__':
    main()
