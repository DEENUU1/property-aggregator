from pydantic import UUID4
from sqlalchemy.orm import Session

from config.database import NotFoundError, AlreadyExistsError
from models.offer import Offer
from repositories.city_repository import CityRepository
from repositories.offer_repository import OfferRepository
from repositories.region_repository import RegionRepository
from schemas.location import RegionInput, CityInput
from schemas.offer import OfferInput, OfferOutput, OfferScraper, OfferList
from enums.offer_sort import OfferSortEnum


class OfferService:

    def __init__(self, session: Session):
        self.repository = OfferRepository(session)
        self.region_repository = RegionRepository(session)
        self.city_repository = CityRepository(session)

    def create(self, offer: OfferInput) -> Offer:
        if self.repository.offer_exists_by_url(offer.details_url):
            raise AlreadyExistsError("Offer already exists")
        offer_obj = self.repository.create(offer)
        return offer_obj

    def create_scraper(self, offer: OfferScraper) -> Offer:
        if self.repository.offer_exists_by_url(offer.details_url):
            raise AlreadyExistsError("Offer already exists")

        if not self.region_repository.region_exists_by_name(offer.region_name):
            self.region_repository.create(RegionInput(name=offer.region_name))
        region = self.region_repository.get_by_name(offer.region_name)

        if not self.city_repository.city_exists_by_name(offer.city_name):
            self.city_repository.create(CityInput(name=offer.city_name, region_id=region.id))
        city = self.city_repository.get_by_name(offer.city_name)

        offer_obj = self.repository.create_scraper(offer, city.id)
        return offer_obj

    def delete(self, _id: int) -> bool:
        if not self.repository.offer_exists_by_id(_id):
            raise NotFoundError("Offer not found")
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

    def get_by_id(self, _id: UUID4) -> OfferOutput:
        if not self.repository.offer_exists_by_id(_id):
            raise NotFoundError("Offer not found")
        return self.repository.get_details(_id)
