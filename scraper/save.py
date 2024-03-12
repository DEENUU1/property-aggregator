from typing import List, Optional, Dict, Any
from enum import Enum
import requests
from model import Offer
import json

class CategoryEnum(str, Enum):
    MIESZKANIE = "Mieszkanie"  # or kawalerka
    POKOJ = "Pokój"
    DOM = "Dom"
    DZIALKA = "DZIAŁKA"
    BIURA_I_LOKALE = "Biura i lokale"
    GARAZE_I_PARKINGI = "Garaże i parkingi"
    STANCJE_I_POKOJE = "Stancje i pokoje"
    HALE_I_MAGAZYNY = "Hale i magazyny"
    POZOSTALE = "Pozostałe"  # Inwestycje


class SubCategoryEnum(str, Enum):
    WYNAJEM = "Wynajem"
    SPRZEDAZ = "Sprzedaż"


class BuildingTypeEnum(str, Enum):
    APARTAMENTOWIEC = "Apartamentowiec"
    BLOK = "Blok"
    KAMIENICA = "Kamienica"
    POZOSTALE = "Pozostałe"
    LOFT = "Loft"


def map_offer(offer: Offer) -> Dict[str, Any]:
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
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/offer",
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


def save_offers(offers: List[Offer]) -> bool:
    for offer in offers:
        mapped_offer = map_offer(offer)
        post(mapped_offer)
