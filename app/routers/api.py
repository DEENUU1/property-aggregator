from fastapi import APIRouter

from routers.v1 import root, region, city, offer

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(root.router)
router.include_router(region.router)
router.include_router(city.router)
router.include_router(offer.router)
