from fastapi import FastAPI

from config.settings import settings
from routers.api import router

app = FastAPI(
    debug=bool(settings.DEBUG),
    title=settings.TITLE,
)

app.include_router(router)
