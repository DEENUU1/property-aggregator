from config.database import Base, engine
from models.favourite import Favorite
from models.location import Region, City
from models.notification import Notification
from models.notification_filter import NotificationFilter
from models.offer import Offer
from models.photo import Photo
from models.user import User


def create_tables():
    """
    Creates all database tables defined in the application.
    """
    Base.metadata.create_all(bind=engine)
    Offer.metadata.create_all(bind=engine)
    Region.metadata.create_all(bind=engine)
    Photo.metadata.create_all(bind=engine)
    City.metadata.create_all(bind=engine)
    User.metadata.create_all(bind=engine)
    Favorite.metadata.create_all(bind=engine)
    NotificationFilter.metadata.create_all(bind=engine)
    Notification.metadata.create_all(bind=engine)
