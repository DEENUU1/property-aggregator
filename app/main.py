from fastapi import FastAPI

from config.database import Base, engine
from config.settings import settings
from routers.api import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    debug=bool(settings.DEBUG),
    title=settings.TITLE,
)

app.include_router(router)
