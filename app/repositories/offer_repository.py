from typing import List, Type

from pydantic import UUID4
from sqlalchemy.orm import Session

from models.offer import Offer
from models.photo import Photo
from schemas.offer import OfferInput, OfferOutput


class OfferRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: OfferInput) -> OfferInput:
        offer = Offer(**data.model_dump(exclude_none=True))
        self.session.add(offer)
        self.session.commit()
        self.session.refresh(offer)
        return OfferInput(**offer.__dict__)

    def offer_exists_by_url(self, url: str) -> bool:
        offer = self.session.query(Offer).filter_by(details_url=url).first()
        if offer:
            return True
        return False

    def offer_exists_by_id(self, _id: UUID4) -> bool:
        offer = self.session.query(Offer).filter_by(id=_id).first()
        if offer:
            return True
        return False

    def get_offer_by_id(self, _id: UUID4) -> Type[Offer]:
        offer = self.session.query(Offer).filter_by(id=_id).first()
        return offer

    def get_details(self, _id: UUID4) -> OfferOutput:
        offer = self.session.query(Offer).filter_by(id=_id).first()
        return OfferOutput(**offer.__dict__)

    def get_all(self) -> List[OfferOutput]:
        offers = self.session.query(Offer).all()
        return [OfferOutput(**offer.__dict__) for offer in offers]

    def delete(self, offer: Type[Offer]) -> bool:
        self.session.delete(offer)
        self.session.commit()
        return True
