from config.database import Base, engine
from models.favourite import Favorite
from models.location import Region, City
from models.offer import Offer
from models.photo import Photo
from models.user import User


def drop_tables():
    Base.metadata.drop_all(bind=engine)
    Offer.metadata.drop_all(bind=engine)
    Region.metadata.drop_all(bind=engine)
    Photo.metadata.drop_all(bind=engine)
    City.metadata.drop_all(bind=engine)
    User.metadata.drop_all(bind=engine)
    Favorite.metadata.drop_all(bind=engine)
