from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config.settings import settings
from routers.api import router
from utils.init_db import create_tables

app = FastAPI(
    debug=bool(settings.DEBUG),
    title=settings.TITLE,
)


@app.on_event("startup")
def on_startup() -> None:
    """
    Initializes the database tables when the application starts up.
    """
    create_tables()


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
