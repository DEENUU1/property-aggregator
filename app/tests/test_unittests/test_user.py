import os
import sys

import pytest

from ..conftest import test_get_db
from repositories.user_repository import UserRepository
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


def test_success_create_user_object(test_get_db, user) -> None:
    assert user.email == "test@example.com"
    assert user.username == "test_user"
    assert user.is_active
    assert user.is_superuser == False


def test_success_user_exists_by_email(test_get_db, user) -> None:
    repository = UserRepository(test_get_db)
    assert repository.user_exists_by_email(user.email)


def test_success_user_exists_by_username(test_get_db, user) -> None:
    repository = UserRepository(test_get_db)
    assert repository.user_exists_by_username(user.username)


def test_success_get_user_by_email(test_get_db, user) -> None:
    repository = UserRepository(test_get_db)
    user = repository.get_user_by_email(user.email)
    assert user.email == "test@example.com"
    assert user.username == "test_user"
    assert user.is_active
    assert user.is_superuser == False


def test_success_get_user_by_username(test_get_db, user) -> None:
    repository = UserRepository(test_get_db)
    user = repository.get_user_by_username(user.username)
    assert user.email == "test@example.com"
    assert user.username == "test_user"
    assert user.is_active
    assert user.is_superuser == False
