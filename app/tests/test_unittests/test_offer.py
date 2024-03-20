import os
import sys

import pytest

from ..conftest import test_get_db
from models.offer import SubCategoryEnum, CategoryEnum, BuildingTypeEnum
from repositories.city_repository import CityRepository
from repositories.offer_repository import OfferRepository
from repositories.region_repository import RegionRepository
from schemas.location import CityInput, RegionInput
from schemas.offer import OfferScraper
from schemas.photo import PhotoInput

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



@pytest.fixture()
def region(test_get_db):
    repository = RegionRepository(test_get_db)
    return repository.create(RegionInput(name="Łódzkie"))


@pytest.fixture()
def city(test_get_db, region):
    repository = CityRepository(test_get_db)
    city_created = repository.create(CityInput(name="Łódź", region_id=region.id))
    city = repository.get_by_name(city_created.name)
    return city


@pytest.fixture()
def offer(test_get_db, city):
    data = OfferScraper(
        title="test offer",
        details_url="https://google.com",
        category=CategoryEnum.POKOJ,
        sub_category=SubCategoryEnum.WYNAJEM,
        building_type=BuildingTypeEnum.POZOSTALE,
        description="test offer",
        price=999.999,
        rent=100,
        price_per_m=100,
        area=100,
        building_floot=1,
        floor=1,
        rooms=1,
        furniture=True,
        photos=[PhotoInput(url="https://google.com/img123")],
        region_name="Łódzkie",
        city_name="Łódź",
    )
    return data


def test_success_create_offer_scraper_object(test_get_db, offer, city) -> None:
    repository = OfferRepository(test_get_db)
    offer = repository.create(offer, city.id)
    assert offer.title == "test offer"
    assert offer.details_url == "https://google.com"
    assert offer.category == CategoryEnum.POKOJ
    assert offer.sub_category == SubCategoryEnum.WYNAJEM
    assert offer.building_type == BuildingTypeEnum.POZOSTALE
    assert offer.price == 999.999
    assert offer.rent == 100
    assert offer.price_per_m == 100
    assert offer.area == 100
    assert offer.building_floot == 1
    assert offer.floor == 1
    assert offer.rooms == 1
    assert offer.furniture == True
    assert offer.photos[0].url == "https://google.com/img123"


def test_success_offer_exists_by_url(test_get_db, offer, city) -> None:
    repository = OfferRepository(test_get_db)
    offer = repository.create(offer, city.id)
    assert repository.offer_exists_by_url(offer.details_url)


def test_success_offer_exists_by_id(test_get_db, offer, city) -> None:
    repository = OfferRepository(test_get_db)
    offer = repository.create(offer, city.id)
    assert repository.offer_exists_by_id(offer.id)
