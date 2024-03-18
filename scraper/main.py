import typer

from data.site import Site
from tasks import run_parser, run_scraper

app = typer.Typer()


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
