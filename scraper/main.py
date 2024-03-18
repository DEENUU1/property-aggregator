import typer

from data.site import Site
from tasks import run_parser, run_scraper
from service import otodom_service, olx_service

app = typer.Typer()


@app.command()
def delete_parsed_olx() -> None:
    service = olx_service.OlxService()
    service.delete_all_parsed()


@app.command()
def delete_parsed_otodom() -> None:
    service = otodom_service.OtodomService()
    service.delete_all_parsed()


@app.command()
def scrape_otodom() -> None:
    run_scraper.run_scrape(Site.OTODOM)


@app.command()
def scrape_olx() -> None:
    run_scraper.run_scrape(Site.OLX)


@app.command()
def parse_otodom() -> None:
    run_parser.run_parser(Site.OTODOM)


@app.command()
def parse_olx() -> None:
    run_parser.run_parser(Site.OLX)


if __name__ == '__main__':
    app()
