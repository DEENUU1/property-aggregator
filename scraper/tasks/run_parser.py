from data.site import Site
from export.save import save_offer
from parser import olx_parser, otodom_parser
from service.olx_service import OlxService
from service.otodom_service import OtodomService
from parser.parser import Parser


def run_parser(site: Site) -> None:
    if site == site.OLX:
        service = OlxService()
        parser = olx_parser.OlxParser()

    elif site == site.OTODOM:
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
        for offer in parse:
            save_offer(offer)
            service.update_parsed(d.get("id"))
            print(f"Offer with id: {d.get("_id")} parsed")
