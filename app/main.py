from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config.database import Base, engine
from config.settings import settings
from routers.api import router

from models.offer import Offer
from models.location import Region, City
from models.photo import Photo
from models.user import User
from models.favourite import Favorite

Base.metadata.create_all(bind=engine)
Offer.metadata.create_all(bind=engine)
Region.metadata.create_all(bind=engine)
Photo.metadata.create_all(bind=engine)
City.metadata.create_all(bind=engine)
User.metadata.create_all(bind=engine)
Favorite.metadata.create_all(bind=engine)

app = FastAPI(
    debug=bool(settings.DEBUG),
    title=settings.TITLE,
)

if settings.DEBUG:
    origins = ["*"]
else:
    origins = [
        str(origin).strip(",") for origin in settings.ORIGINS
    ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
