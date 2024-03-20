import typer

from data.site import Site
from service import otodom_service, olx_service
from tasks import run_parser, run_scraper

app = typer.Typer()


@app.command()
def delete_parsed_olx() -> None:
    """
    Delete all parsed data from OLX service.
    """
    service = olx_service.OlxService()
    service.delete_all_parsed()


@app.command()
def delete_parsed_otodom() -> None:
    """
    Delete all parsed data from Otodom service.
    """
    service = otodom_service.OtodomService()
    service.delete_all_parsed()


@app.command()
def scrape_otodom() -> None:
    """
    Scrape data from Otodom website.
    """
    run_scraper.run_scrape(Site.OTODOM)


@app.command()
def scrape_olx() -> None:
    """
    Scrape data from OLX website.
    """
    run_scraper.run_scrape(Site.OLX)


@app.command()
def parse_otodom() -> None:
    """
    Parse data from Otodom website.
    """
    run_parser.run_parser(Site.OTODOM)


@app.command()
def parse_olx() -> None:
    """
    Parse data from OLX website.
    """
    run_parser.run_parser(Site.OLX)


if __name__ == '__main__':
    app()
