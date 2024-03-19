import os
import sys

import pytest
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator, Any
from fastapi.testclient import TestClient


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import offer, location, user, favourite, photo, notification, notification_filter
from main import app
from config.database import get_db
from routers.api import router
from utils.init_db import create_tables


engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def test_init_db() -> None:
    offer.Offer.metadata.create_all(bind=engine)
    location.Region.metadata.create_all(bind=engine)
    location.City.metadata.create_all(bind=engine)
    photo.Photo.metadata.create_all(bind=engine)
    user.User.metadata.create_all(bind=engine)
    favourite.Favorite.metadata.create_all(bind=engine)
    notification.Notification.metadata.create_all(bind=engine)
    notification_filter.NotificationFilter.metadata.create_all(bind=engine)

def start_app():
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture()
def app() -> Generator:
    create_tables()
    _app = start_app()
    yield _app


@pytest.fixture
def test_get_db():
    test_init_db()
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        engine.dispose()

SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()




@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """
    test_init_db()

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client
