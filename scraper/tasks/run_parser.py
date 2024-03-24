from data.site import Site
from export.save import save_offer
from parser import olx_parser, otodom_parser
from parser.parser import Parser
from service.olx_service import OlxService
from service.otodom_service import OtodomService


def run_parser(site: Site) -> None:
    """
    Run the parser for the specified site.

    Args:
        site (Site): The site to parse.

    Returns:
        None
    """
    if site == Site.OLX:
        service = OlxService()
        parser = olx_parser.OlxParser()

    elif site == Site.OTODOM:
        service = OtodomService()
        parser = otodom_parser.OtodomParser()

    else:
        raise ValueError(f"Unknown site: {site}")

    for d in service.get_all_unparsed():
        # Get 'data' field from collection
        data = d.get("data", None)
        # Get 'category' and 'sub_category' fields from collection
        category, sub_category = d.get("category", None), d.get("sub_category", None)

        parse = Parser(parser).parse(data, category=category, sub_category=sub_category)
        save_offer(parse)
        service.update_parsed(d.get("id"))
        print(f"Offer with id: {d.get('_id')} parsed")
