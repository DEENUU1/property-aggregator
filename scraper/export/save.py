import json
from typing import Dict, Any

import requests

from data.offer import Offer


def map_offer(offer: Offer) -> Dict[str, Any]:
    """
    Map Offer object attributes to a dictionary.

    Args:
        offer (Offer): The offer object to be mapped.

    Returns:
        Dict[str, Any]: A dictionary containing mapped offer data.
    """
    photos = [{"url": item} for item in offer.photos]
    data = {
        "title": offer.title,
        "details_url": offer.url,
        "category": offer.category,
        "sub_category": offer.sub_category,
        "building_type": offer.building_type,
        "price": offer.price,
        "rent": offer.rent,
        "description": offer.description,
        "price_per_m": offer.price_per_meter,
        "area": offer.area,
        "building_floot": offer.building_floor,
        "floor": offer.floor,
        "rooms": offer.room_number,
        "furniture": offer.has_furnitures,
        "photos": photos,
        "region_name": offer.location.region,
        "city_name": offer.location.city
    }
    return data


def post(offer: Dict[str, Any]) -> bool:
    """
    Post offer data to the server.

    Args:
        offer (Dict[str, Any]): A dictionary containing offer data.

    Returns:
        bool: True if the offer is successfully saved, False otherwise.
    """
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/offer/scraper",
            data=json.dumps(offer),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )
        response.raise_for_status()
        if response.status_code != 200:
            print(f"Offer not saved, {response.status_code}")
            return False
        print("Offer saved")
        return True
    except requests.ConnectionError as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def save_offer(offer: Offer) -> bool:
    """
    Save offer by mapping, then posting it to the server.

    Args:
        offer (Offer): The offer object to be saved.
    """
    try:
        mapped_offer = map_offer(offer)
        post(mapped_offer)
        return True
    except Exception as e:
        print(f"Save offer error: {e}")
        return False
