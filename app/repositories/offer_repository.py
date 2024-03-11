from typing import List, Type, Dict, Any

from pydantic import UUID4
from sqlalchemy.orm import Session
from models.offer import Offer
from schemas.offer import OfferInput, OfferOutput
from models.photo import Photo


class OfferRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: OfferInput) -> Offer:
        db_offer = Offer(**data.model_dump(exclude_none=True, exclude={"photos"}))
        self.session.add(db_offer)
        self.session.commit()
        self.session.refresh(db_offer)

        for photo in data.photos:
            db_photo = Photo(url=photo.url, offer_id=db_offer.id)
            self.session.add(db_photo)
            self.session.commit()
            self.session.refresh(db_photo)

        return db_offer

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

    def get_all(self) -> List[Dict[str, List[Dict[str, Any]] | Any]]:
        offers = self.session.query(Offer).all()

        offer_list = []
        for offer in offers:
            photo_list = [{"url": photo.url} for photo in offer.photos]
            offer_list.append({
                "id": offer.id,
                "title": offer.title,
                "details_url": offer.details_url,
                "category": offer.category,
                "sub_category": offer.sub_category,
                "building_type": offer.building_type,
                "price": offer.price,
                "rent": offer.rent,
                "description": offer.description,
                "price_per_m": offer.price_per_m,
                "area": offer.area,
                "building_floor": offer.building_floot,
                "floor": offer.floor,
                "rooms": offer.rooms,
                "furniture": offer.furniture,
                "photos": photo_list,
                # "city": offer.city_id,
            })

        return offer_list

    def delete(self, offer: Type[Offer]) -> bool:
        self.session.delete(offer)
        self.session.commit()
        return True
