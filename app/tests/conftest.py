import os
import sys

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import offer, location, user, favourite, photo, notification, notification_filter

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# @pytest.fixture()
# def client() -> Generator:
#     with TestClient(app) as c:
#         app.dependency_overrides[get_current_user] = override_get_current_user
#         yield c
#         app.dependency_overrides = {}


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
