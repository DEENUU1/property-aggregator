from typing import Dict, Any

from pydantic import UUID4
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.offer import Offer
from repositories.city_repository import CityRepository
from repositories.offer_repository import OfferRepository
from repositories.region_repository import RegionRepository
from schemas.location import RegionInput, CityInput
from schemas.offer import OfferOutput, OfferScraper, OfferList
from enums.offer_sort import OfferSortEnum
from schemas.user import UserIn
from services.user_service import UserService


class OfferService:

    def __init__(self, session: Session):
        self.repository = OfferRepository(session)
        self.region_repository = RegionRepository(session)
        self.city_repository = CityRepository(session)
        self.user_service = UserService(session)

    def create(self, offer: OfferScraper) -> Offer:
        if self.repository.offer_exists_by_url(offer.details_url):
            raise HTTPException(status_code=400, detail="Offer already exists")

        if not self.region_repository.region_exists_by_name(offer.region_name):
            self.region_repository.create(RegionInput(name=offer.region_name))
        region = self.region_repository.get_by_name(offer.region_name)

        if not self.city_repository.city_exists_by_name(offer.city_name):
            self.city_repository.create(CityInput(name=offer.city_name, region_id=region.id))
        city = self.city_repository.get_by_name(offer.city_name)

        offer_obj = self.repository.create(offer, city.id)
        return offer_obj

    def delete(self, _id: int, user_id: UUID4) -> bool:
        if not self.user_service.is_superuser(user_id):
            raise HTTPException(status_code=403, detail="Forbidden")

        if not self.repository.offer_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Offer not found")
        offer = self.repository.get_offer_by_id(_id)
        self.repository.delete(offer)
        return True

    def get_all(
            self,
            offset: int = 1,
            page_size: int = 15,
            category: str = None,
            sub_category: str = None,
            building_type: str = None,
            price_min: int = None,
            price_max: int = None,
            area_min: int = None,
            area_max: int = None,
            rooms: int = None,
            furniture: bool = None,
            floor: int = None,
            query: str = None,
            sort_by: OfferSortEnum = OfferSortEnum.NEWEST
    ) -> OfferList:
        return self.repository.get_all(
            offset,
            page_size,
            category,
            sub_category,
            building_type,
            price_min,
            price_max,
            area_min,
            area_max,
            rooms,
            furniture,
            floor,
            query,
            sort_by
        )

    def get_by_id(self, _id: UUID4) -> Dict[str, Any]:
        if not self.repository.offer_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Offer not found")
        return self.repository.get_details(_id)
