from fastapi import APIRouter

from routers.v1 import root, region, city, offer, user, favourite, notification, statistic

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(root.router)
router.include_router(region.router)
router.include_router(city.router)
router.include_router(offer.router)
router.include_router(user.router)
router.include_router(favourite.router)
router.include_router(notification.router)
router.include_router(statistic.router)
