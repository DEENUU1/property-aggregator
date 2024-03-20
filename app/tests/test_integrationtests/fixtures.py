import pytest

from auth.security import get_password_hash
from models.offer import CategoryEnum, SubCategoryEnum, BuildingTypeEnum
from repositories.city_repository import CityRepository
from repositories.offer_repository import OfferRepository
from repositories.region_repository import RegionRepository
from repositories.user_repository import UserRepository
from schemas.location import RegionInput, CityInput
from schemas.offer import OfferScraper
from schemas.photo import PhotoInput
from schemas.user import UserIn
from schemas.favourite import FavouriteInput
from repositories.favourite_repository import FavouriteRepository
from repositories.notification_repository import NotificationRepository
from repositories.notificationfilter_repository import NotificationFilterRepository
from schemas.notification import NotificationInput
from schemas.notification_filter import NotificationFilterInput


@pytest.fixture(scope="function")
def region(client):
    test_client, db_session = client

    region = RegionRepository(db_session).create(RegionInput(name="Łódzkie"))
    return region


@pytest.fixture(scope="function")
def city(client, region):
    test_client, db_session = client

    city = CityRepository(db_session).create(CityInput(name="Łódź", region_id=region.id))
    return city


@pytest.fixture(scope="function")
def offer(client, city):
    test_client, test_session = client
    photo_input = PhotoInput(url="https://google.com/img/123")

    data = OfferScraper(
        title="string",
        details_url="string",
        category=CategoryEnum.MIESZKANIE,
        sub_category=SubCategoryEnum.WYNAJEM,
        building_type=BuildingTypeEnum.BLOK,
        price=1000.00,
        rent=200,
        description="test",
        price_per_m=300,
        area=1000,
        building_floot=10,
        floor=1,
        rooms=2,
        photos=[photo_input],
        region_name="Łódzkie",
        city_name="Łódź",
    )
    return OfferRepository(test_session).create(data, city.id)


@pytest.fixture(scope="function")
def user_admin(client):
    test_client, db_session = client

    password = "XXXX"
    hashed_password = get_password_hash(password)

    user = UserRepository(db_session).create(
        UserIn(
            email="test@example.com",
            password=password,
            username="XXXX",
            is_superuser=True,
        ),
        hashed_password=hashed_password
    )
    return user


@pytest.fixture(scope="function")
def user(client):
    test_client, db_session = client

    password = "XXXX"
    hashed_password = get_password_hash(password)

    user = UserRepository(db_session).create(
        UserIn(
            email="test2@example.com",
            password=password,
            username="XXXX2",
        ),
        hashed_password=hashed_password
    )
    return user


@pytest.fixture(scope="function")
def user_admin_access_token(user_admin, client):
    test_client, db_session = client

    data = {'grant_type': '', 'username': 'XXXX', 'password': "XXXX", 'scope': '', 'client_id': '',
            'client_secret': ''}
    access_token = test_client.post(
        "/api/v1/user/login",
        data=data,
    ).json()["access_token"]
    return access_token


@pytest.fixture(scope="function")
def user_access_token(user, client):
    test_client, db_session = client

    data = {'grant_type': '', 'username': 'XXXX2', 'password': "XXXX", 'scope': '', 'client_id': '',
            'client_secret': ''}
    access_token = test_client.post(
        "/api/v1/user/login",
        data=data,
    ).json()["access_token"]
    return access_token


@pytest.fixture(scope="function")
def favourite(client, user, offer):
    test_client, db_session = client

    return FavouriteRepository(db_session).create(FavouriteInput(user_id=user.id, offer_id=offer.id))


@pytest.fixture(scope="function")
def notification(client, user, offer):
    test_client, db_session = client

    return NotificationRepository(db_session).create(
        NotificationInput(
            user_id=user.id,
            title="New 4 offers",
            message="test message"
        )
    )


@pytest.fixture(scope="function")
def notification_filter(client, user):
    test_client, db_session = client

    return NotificationFilterRepository(db_session).create(
        NotificationFilterInput(
            user_id=user.id,
            category=CategoryEnum.MIESZKANIE,
        )
    )


offer_data = {
    "title": "string",
    "details_url": "string",
    "category": "Mieszkanie",
    "sub_category": "Wynajem",
    "building_type": "Apartamentowiec",
    "price": 0,
    "rent": 0,
    "description": "string",
    "price_per_m": 0,
    "area": 0,
    "building_floot": 0,
    "floor": 0,
    "rooms": 0,
    "furniture": True,
    "photos": [
        {
            "url": "string"
        }
    ],
    "region_name": "string",
    "city_name": "string"
}