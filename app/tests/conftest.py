from typing import Generator
from unittest.mock import MagicMock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys
from fastapi.testclient import TestClient


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import offer, location, user, favourite, photo, notification, notification_filter
from main import app
from schemas.user import UserIn, UserInDBBase
from auth.auth import get_current_user

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def override_get_current_user() -> UserInDBBase:  # Return a real UserIn object
    user = UserInDBBase(id="279dcf76-a100-48b2-9fd4-f891d5093f4c", email="test@example.com", username="test", password="test")
    return user


@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as c:
        app.dependency_overrides[get_current_user] = override_get_current_user
        yield c
        app.dependency_overrides = {}


def test_init_db() -> None:
    offer.Offer.metadata.create_all(bind=engine)
    location.Region.metadata.create_all(bind=engine)
    location.City.metadata.create_all(bind=engine)
    photo.Photo.metadata.create_all(bind=engine)
    user.User.metadata.create_all(bind=engine)
    favourite.Favorite.metadata.create_all(bind=engine)
    notification.Notification.metadata.create_all(bind=engine)
    notification_filter.NotificationFilter.metadata.create_all(bind=engine)


@pytest.fixture
def test_get_db():
    test_init_db()
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        engine.dispose()
