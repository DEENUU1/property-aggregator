from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config.settings import settings
from routers.api import router
from utils.init_db import create_tables

create_tables()

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
    app_configs = {"openapi_url": None}
    app = FastAPI(**app_configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
