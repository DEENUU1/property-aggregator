from fastapi import APIRouter

from routers.v1 import root, region

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(root.router)
router.include_router(region.router)