from typing import List

from pydantic import UUID4
from sqlalchemy.orm import Session

from config.database import NotFoundError, AlreadyExistsError
from repositories.offer_repository import OfferRepository
from schemas.offer import OfferInput, OfferOutput


class OfferService:

    def __init__(self, session: Session):
        self.repository = OfferRepository(session)

    def create(self, offer: OfferInput) -> OfferInput:
        if self.repository.offer_exists_by_url(offer.details_url):
            raise AlreadyExistsError("Offer already exists")
        offer_obj = self.repository.create(offer)
        return offer_obj

    def delete(self, _id: int) -> bool:
        if not self.repository.offer_exists_by_id(_id):
            raise NotFoundError("Offer not found")
        offer = self.repository.get_offer_by_id(_id)
        self.repository.delete(offer)
        return True

    def get_all(self) -> List[OfferOutput]:
        return self.repository.get_all()

    def get_by_id(self, _id: UUID4) -> OfferOutput:
        if not self.repository.offer_exists_by_id(_id):
            raise NotFoundError("Offer not found")
        return self.repository.get_details(_id)
