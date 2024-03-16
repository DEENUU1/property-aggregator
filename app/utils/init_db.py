from config.database import Base, engine
from models.favourite import Favorite
from models.location import Region, City
from models.offer import Offer
from models.photo import Photo
from models.user import User
from models.notification import Notification


def create_tables():
    Base.metadata.create_all(bind=engine)
    Offer.metadata.create_all(bind=engine)
    Region.metadata.create_all(bind=engine)
    Photo.metadata.create_all(bind=engine)
    City.metadata.create_all(bind=engine)
    User.metadata.create_all(bind=engine)
    Favorite.metadata.create_all(bind=engine)
    Notification.metadata.create_all(bind=engine)

