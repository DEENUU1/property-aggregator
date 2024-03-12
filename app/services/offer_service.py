from typing import List, Dict, Any

from pydantic import UUID4
from sqlalchemy.orm import Session

from config.database import NotFoundError, AlreadyExistsError
from repositories.offer_repository import OfferRepository
from schemas.offer import OfferInput, OfferOutput, OfferScraper
from models.offer import Offer
from repositories.region_repository import RegionRepository
from schemas.location import RegionInput, CityInput
from repositories.city_repository import CityRepository


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

    def get_all(self) -> List[Dict[str, List[Dict[str, Any]] | Any]]:
        return self.repository.get_all()

    def get_by_id(self, _id: UUID4) -> OfferOutput:
        if not self.repository.offer_exists_by_id(_id):
            raise NotFoundError("Offer not found")
        return self.repository.get_details(_id)
