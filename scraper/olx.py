from typing import Any, List, Dict, Optional, Union, Tuple
from model import Offer, Location
import requests

BASE_URL = "https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=3&filter_refiners=spell_checker&sl=18c34ade124x23bc10a5"


def get_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(e)
        return None
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    except Exception as e:
        print(e)
        return None


def get_next_page_url(content: Dict[str, Any]) -> Optional[str]:
    links = content.get("links", None)
    if not links:
        return None
    next_url = links.get("next", None)
    if not next_url:
        return None
    url = next_url.get("href")
    print(url)
    return url


def parse_page(content) -> List[Optional[Offer]]:
    offers = content.get("data", None)
    parsed_offers = []

    for offer in offers:
        url = offer.get("url", None)
        title = offer.get("title", None)

        if url is None or title is None:
            continue

        description = offer.get("description", None)

        map_data = offer.get("map")
        lat = map_data.get("lat")
        lon = map_data.get("lon")

        location_data = offer.get("location")
        city_name = location_data.get("city").get("name")
        region_name = location_data.get("region").get("name")

        photo_data = offer.get("photos", None)
        photos = []
        for photo in photo_data:
            link = photo.get("link", None)
            width = photo.get("width", None)
            height = photo.get("height", None)

            full_link = link.format(width=width, height=height)
            photos.append(full_link)

        params_data = offer.get("params", None)
        parsed_params = []
        for param in params_data:
            label_keys = ["roomsize", "floor_select", "builttype", "floor", "type"]

            key_name = param.get("key", None)
            if key_name == "price":
                value = param.get("value", None).get("value", None)
            elif key_name in label_keys:
                value = param.get("value").get("label")
            else:
                value = param.get("value").get("key")
                if value == "yes" or value == "no":
                    value = True if value == "yes" else False

            param = {"key_name": key_name, "value": value}
            parsed_params.append(param)

        location = Location(city=city_name, region=region_name, lat=lat, lon=lon)
        offer = Offer(
            url=url,
            title=title,
            location=location,
            photos=photos,
            description=description,
            price_per_meter=get_param_value(parsed_params, "price_per_m"),
            meters=get_param_value(parsed_params, "m"),
            price=get_param_value(parsed_params, "price"),
            area=get_param_value(parsed_params, "area"),
            building_type=get_param_value(parsed_params, "builttype"),
            building_floor=get_param_value(parsed_params, "floor_select"),
            floor=get_param_value(parsed_params, "floor"),
            room_number=get_param_value(parsed_params, "rooms"),
            has_furnitures=get_param_value(parsed_params, "furniture"),
            type=get_param_value(parsed_params, "type"),
        )
        print(offer)
        parsed_offers.append(offer)
    return parsed_offers


def get_param_value(params: List[Dict[str, Any]], key: str) -> Any:
    for param in params:
        if key in param["key_name"]:
            return param["value"]


def run():
    page_num = 1

    init_page = get_content(BASE_URL)
    parsed_data = parse_page(init_page)
    next_page = get_next_page_url(init_page)
    while next_page:
        content = get_content(next_page)
        next_page = get_next_page_url(content)
        print(next_page)
        if not next_page:
            break
        parsed_data = parse_page(content)
        page_num += 1


if __name__ == "__main__":
    run()

