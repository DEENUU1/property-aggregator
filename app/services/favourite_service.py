from typing import List

from pydantic import UUID4
from sqlalchemy.orm import Session
from fastapi import HTTPException
from repositories.favourite_repository import FavouriteRepository
from schemas.favourite import FavouriteInput, FavouriteOfferOutput
from repositories.offer_repository import OfferRepository
from services.user_service import UserService


class FavouriteService:

    def __init__(self, session: Session):
        self.repository = FavouriteRepository(session)
        self.repository_offer = OfferRepository(session)
        self.user_service = UserService(session)

    def create(self, data: FavouriteInput) -> FavouriteInput:
        if self.repository.offer_saved_by_user(data.user_id, data.offer_id):
            raise HTTPException(status_code=400, detail="Offer already saved")

        if not self.repository_offer.offer_exists_by_id(data.offer_id):
            raise HTTPException(status_code=404, detail="Offer not found")

        favourite = self.repository.create(data)
        return FavouriteInput(**favourite.__dict__)

    def delete(self, _id: UUID4, user_id: UUID4) -> bool:
        if not self.repository.favourite_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Favourite not found")

        favourite = self.repository.get_favourite(_id)

        if favourite.user_id != user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        return self.repository.delete(favourite)

    def get_all_by_user(self, user_id: UUID4) -> List[FavouriteOfferOutput]:
        favourites = self.repository.get_all_by_user(user_id)

        results = []
        for favourite in favourites:
            result = self.repository_offer.get_details(favourite.offer_id)
            favourite_offer = FavouriteOfferOutput(id=favourite.id, offer=result)
            results.append(favourite_offer)

        return results
