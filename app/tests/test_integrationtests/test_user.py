from auth.security import get_password_hash
from repositories.user_repository import UserRepository
from schemas.user import UserIn


def test_success_return_201_status_code_register(client) -> None:
    test_client, db_session = client

    response = test_client.post(
        "/api/v1/user/register",
        json={
            "email": "test@example.com",
            "password": "test",
            "username": "test",
        },
    )
    assert response.status_code == 201


def test_error_return_status_code_400_register_create_user_with_already_used_email_address(client) -> None:
    test_client, db_session = client

    UserRepository(db_session).create(
        UserIn(
            email="test@example.com",
            password="XXXX",
            username="test123"),
        hashed_password="asd"
    )

    response = test_client.post(
        "/api/v1/user/register",
        json={
            "email": "test@example.com",
            "password": "XXXX",
            "username": "XXXX",
        },
    )
    assert response.status_code == 400


def test_error_return_status_code_400_register_create_user_with_already_used_username_address(client) -> None:
    test_client, db_session = client

    UserRepository(db_session).create(
        UserIn(
            email="test123@example.com",
            password="XXXX",
            username="XXXX"),
        hashed_password="asd"
    )

    response = test_client.post(
        "/api/v1/user/register",
        json={
            "email": "test@example.com",
            "password": "XXXX",
            "username": "XXXX",
        },
    )
    assert response.status_code == 400


def test_success_return_status_code_201_login(client) -> None:
    test_client, db_session = client

    password = "XXXX"
    hashed_password = get_password_hash(password)

    UserRepository(db_session).create(
        UserIn(
            email="test@example.com",
            password=password,
            username="XXXX"),
        hashed_password=hashed_password
    )
    data = {'grant_type': '', 'username': 'XXXX', 'password': password, 'scope': '', 'client_id': '',
            'client_secret': ''}
    response = test_client.post(
        "/api/v1/user/login",
        data=data
    )
    assert response.status_code == 201


def test_error_return_status_code_401_login_user_account_does_not_exist(client) -> None:
    test_client, db_session = client

    data = {'grant_type': '', 'username': 'XXXX', 'password': 'XXXX', 'scope': '', 'client_id': '',
            'client_secret': ''}
    response = test_client.post(
        "/api/v1/user/login",
        data=data
    )
    assert response.status_code == 401


def test_error_return_status_code_return_status_code_401_login_user_account_invalid_password(client) -> None:
    test_client, db_session = client

    password = "XXXX"
    hashed_password = get_password_hash(password)

    UserRepository(db_session).create(
        UserIn(
            email="test@example.com",
            password=password,
            username="XXXX"),
        hashed_password=hashed_password
    )
    data = {'grant_type': '', 'username': 'XXXX', 'password': 'invalidPassword', 'scope': '', 'client_id': '',
            'client_secret': ''}
    response = test_client.post(
        "/api/v1/user/login",
        data=data
    )
    assert response.status_code == 401


def test_success_return_status_code_200_get_me(client) -> None:
    test_client, db_session = client

    password = "XXXX"
    hashed_password = get_password_hash(password)

    UserRepository(db_session).create(
        UserIn(
            email="test@example.com",
            password=password,
            username="XXXX"),
        hashed_password=hashed_password
    )
    data = {'grant_type': '', 'username': 'XXXX', 'password': password, 'scope': '', 'client_id': '',
            'client_secret': ''}
    response = test_client.post(
        "/api/v1/user/login",
        data=data
    )
    access_token = response.json()["access_token"]
    response = test_client.get(
        "/api/v1/user/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200


def test_success_return_status_code_204_delete_me(client) -> None:
    test_client, db_session = client

    password = "XXXX"
    hashed_password = get_password_hash(password)

    UserRepository(db_session).create(
        UserIn(
            email="test@example.com",
            password=password,
            username="XXXX"),
        hashed_password=hashed_password
    )
    data = {'grant_type': '', 'username': 'XXXX', 'password': password, 'scope': '', 'client_id': '',
            'client_secret': ''}
    response = test_client.post(
        "/api/v1/user/login",
        data=data
    )
    access_token = response.json()["access_token"]
    response = test_client.delete(
        "/api/v1/user/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 204
