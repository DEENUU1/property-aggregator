import pytest
from repositories.user_repository import UserRepository
from schemas.user import UserIn
from auth.security import get_password_hash
from repositories.region_repository import RegionRepository
from schemas.location import RegionInput


@pytest.fixture(scope="function")
def region(client):
    test_client, db_session = client

    region = RegionRepository(db_session).create(RegionInput(name="Łódzkie"))
    return region


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
def user_access_token(user_admin, client):
    test_client, db_session = client

    data = {'grant_type': '', 'username': 'XXXX2', 'password': "XXXX", 'scope': '', 'client_id': '',
            'client_secret': ''}
    access_token = test_client.post(
        "/api/v1/user/login",
        data=data,
    ).json()["access_token"]
    return access_token
