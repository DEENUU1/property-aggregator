import pytest
# from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import offer, location, user, favourite, photo


# client = TestClient(app)

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

offer.Offer.metadata.create_all(bind=engine)
location.Region.metadata.create_all(bind=engine)
location.City.metadata.create_all(bind=engine)
photo.Photo.metadata.create_all(bind=engine)
user.User.metadata.create_all(bind=engine)
favourite.Favorite.metadata.create_all(bind=engine)


@pytest.fixture
def test_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
