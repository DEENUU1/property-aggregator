from typing import Type

from pydantic import UUID4
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from enums.offer_sort import OfferSortEnum
from models.offer import Offer
from models.photo import Photo
from schemas.location import CityOutput, RegionOutput
from schemas.offer import OfferInput, OfferOutput, OfferScraper, OfferList


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

    def create_scraper(self, data: OfferScraper, city_id: str) -> Offer:
        db_offer = Offer(**data.model_dump(exclude_none=True, exclude={"photos", "region_name", "city_name"}))
        db_offer.city_id = city_id
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

    def get_all(
            self,
            offset: int = 1,
            page_limit: int = 15,
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
            sort_by: OfferSortEnum = OfferSortEnum.NEWEST,
    ) -> OfferList:
        offers = self.session.query(Offer)

        if query:
            offers = offers.filter(Offer.title.like(f"%{query}%"))

        if category:
            offers = offers.filter(Offer.category == category)
        if sub_category:
            offers = offers.filter(Offer.sub_category == sub_category)
        if building_type:
            offers = offers.filter(Offer.building_type == building_type)
        if price_min:
            offers = offers.filter(Offer.price >= price_min)
        if price_max:
            offers = offers.filter(Offer.price <= price_max)
        if area_min:
            offers = offers.filter(Offer.area >= area_min)
        if area_max:
            offers = offers.filter(Offer.area <= area_max)
        if rooms:
            offers = offers.filter(Offer.rooms == rooms)
        if furniture is not None:
            offers = offers.filter(Offer.furniture == furniture)
        if floor:
            offers = offers.filter(Offer.floor == floor)

        if sort_by == OfferSortEnum.NEWEST:
            offers = offers.order_by(desc(Offer.created_at))
        elif sort_by == OfferSortEnum.OLDEST:
            offers = offers.order_by(asc(Offer.created_at))
        elif sort_by == OfferSortEnum.PRICE_LOWEST:
            offers = offers.order_by(asc(Offer.price))
        elif sort_by == OfferSortEnum.PRICE_HIGHEST:
            offers = offers.order_by(desc(Offer.price))

        offers = offers.offset(offset).limit(page_limit).all()

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
                "city": CityOutput(
                    id=offer.city.id,
                    name=offer.city.name,
                    region=RegionOutput(
                        id=offer.city.region.id, name=offer.city.region.name
                    )
                ),
                "created_at": offer.created_at,
                "updated_at": offer.updated_at
            })

        result = OfferList(offers=offer_list, page=offset, page_size=len(offer_list))
        return result

    def delete(self, offer: Type[Offer]) -> bool:
        self.session.delete(offer)
        self.session.commit()
        return True
