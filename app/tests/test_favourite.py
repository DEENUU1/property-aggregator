import os
import sys

import pytest

from conftest import test_get_db
from models.offer import BuildingTypeEnum, CategoryEnum, SubCategoryEnum
from repositories.city_repository import CityRepository
from repositories.favourite_repository import FavouriteRepository
from repositories.offer_repository import OfferRepository
from repositories.region_repository import RegionRepository
from repositories.user_repository import UserRepository
from schemas.favourite import FavouriteInput
from schemas.location import CityInput, RegionInput
from schemas.offer import OfferScraper
from schemas.photo import PhotoInput
from schemas.user import UserIn

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture()
def user(test_get_db):
    repository = UserRepository(test_get_db)
    hashed_password = "test_hasshed_password"
    user = repository.create(
        UserIn(
            email="test@example.com",
            username="test_user",
            password="test_password"
        ),
        hashed_password=hashed_password
    )
    return user


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

    repository = OfferRepository(test_get_db)
    offer = repository.create_scraper(data, city.id)
    return offer


def test_success_create_favourite_object(test_get_db, offer, user):
    repository = FavouriteRepository(test_get_db)
    favourite = repository.create(FavouriteInput(user_id=user.id, offer_id=offer.id))
    assert favourite.user_id == user.id
    assert favourite.offer_id == offer.id


def test_get_all_by_user(test_get_db, offer, user):
    repository = FavouriteRepository(test_get_db)
    repository.create(FavouriteInput(user_id=user.id, offer_id=offer.id))

    user_favourites = repository.get_all_by_user(user.id)
    assert len(user_favourites) == 1
    assert user_favourites[0].offer_id == offer.id
