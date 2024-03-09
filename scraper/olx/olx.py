import json
from dataclasses import dataclass
from typing import Any, List, Dict, Optional

import requests

BASE_URL = "https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=3&filter_refiners=spell_checker&sl=18c34ade124x23bc10a5"


@dataclass
class Location:
    city: str
    region: str
    lat: float
    lon: float


@dataclass
class Param:
    price_value: Optional[int] = None
    price_currency: Optional[str] = None
    key_name: Optional[str] = None
    value: Optional[str] = None


@dataclass
class Offer:
    url: str
    title: str
    location: Location
    photos: List[str]
    description: Optional[str] = None
    params: List[Optional[Param]] = None


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

            price_value, price_currency, value_label, value_key = None, None, None, None

            key_name = param.get("key", None)
            if key_name == "price":
                price_value = param.get("value", None).get("value", None)
                price_currency = param.get("value", None).get("currency", None)
            elif key_name in label_keys:
                value_label = param.get("value").get("label")
            else:
                value_key = param.get("value").get("key")
                if value_key == "yes" or value_key == "no":
                    value_key = True if value_key == "yes" else False

            value = None
            if value_label:
                value = value_label
            if value_key:
                value = value_key

            param = Param(
                price_value=price_value,
                price_currency=price_currency,
                key_name=key_name,
                value=value
            )
            parsed_params.append(param)

        location = Location(city=city_name, region=region_name, lat=lat, lon=lon)
        offer = Offer(
            url=url,
            title=title,
            location=location,
            photos=photos,
            description=description,
            params=parsed_params
        )
        parsed_offers.append(offer)
    return parsed_offers


def export_to_json(offers: List[Offer], page_num: int):
    offer_dicts = []
    for offer in offers:
        offer_dict = {
            "url": offer.url,
            "title": offer.title,
            "location": {
                "city": offer.location.city,
                "region": offer.location.region,
                "lat": offer.location.lat,
                "lon": offer.location.lon,
            },
            "photos": offer.photos,
            "description": offer.description,
            "params": [
                {
                    "price_value": param.price_value,
                    "price_currency": param.price_currency,
                    "key_name": param.key_name,
                    "value": param.value,
                }
                if param else None
                for param in offer.params
            ] if offer.params else None
        }
        offer_dicts.append(offer_dict)

    with open(f"./data/{page_num}.json", "w", encoding="utf-8") as json_file:
        json.dump(offer_dicts, json_file, indent=4)


def run():
    page_num = 1

    init_page = get_content(BASE_URL)
    parsed_data = parse_page(init_page)
    export_to_json(parsed_data, page_num)
    next_page = get_next_page_url(init_page)
    while next_page:
        content = get_content(next_page)
        next_page = get_next_page_url(content)
        print(next_page)
        if not next_page:
            break
        parsed_data = parse_page(content)
        export_to_json(parsed_data, page_num)
        page_num += 1


def get_json_data(file_path):
    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data


def get_all_unique_params():

    unique = []
    visited = set()

    for i in range(1, 25):
        with open(f"./data/{i}.json", "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        for offer in data:
            params = offer.get("params", None)
            if not params:
                continue

            for param in params:
                key_name = param.get("key_name", None)
                value = param.get("value", None)

                if key_name and value:
                    if key_name not in visited:
                        visited.add(key_name)
                        unique.append({"key_name": key_name, "value": value})

    for u in unique:
        print(u)


# {'key_name': 'price_per_m', 'value': '5205.13'}
# {'key_name': 'market', 'value': 'primary'}
# {'key_name': 'm', 'value': '117'}
# {'key_name': 'area', 'value': '170'}
# {'key_name': 'builttype', 'value': 'Szeregowiec'}
# {'key_name': 'floor_select', 'value': 'Parterowy z użytkowym poddaszem'}
# {'key_name': 'rooms', 'value': 'one'}
# {'key_name': 'furniture', 'value': True}
# {'key_name': 'roomsize', 'value': 'Jednoosobowy'}
# {'key_name': 'preferences', 'value': 'women'}
# {'key_name': 'rent', 'value': '500'}
# {'key_name': 'floor', 'value': 'Parter'}
# {'key_name': 'type', 'value': 'Biurowe'}
# {'key_name': 'rodzaj_nieruchomosci', 'value': 'house'}
# {'key_name': 'rodzajtransakcji', 'value': 'sale'}
# {'key_name': 'kraj', 'value': 'spain'}
# {'key_name': 'lazienki', 'value': '1'}
# {'key_name': 'surroundings', 'value': ['sea', 'lake']}
# {'key_name': 'amenit_re', 'value': ['balcony', 'terrace']}
# {'key_name': 'contactlanguage', 'value': ['polish']}


if __name__ == "__main__":
    # run()
    get_all_unique_params()