from fastapi import APIRouter

from routers.v1 import root

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(root.router)
