from pydantic import UUID4
from sqlalchemy.orm import Session
from fastapi import HTTPException
from repositories.favourite_repository import FavouriteRepository
from schemas.favourite import FavouriteInput, FavouriteListOutput
from repositories.offer_repository import OfferRepository


class FavouriteService:

    def __init__(self, session: Session):
        self.repository = FavouriteRepository(session)
        self.repository_offer = OfferRepository(session)

    def create(self, data: FavouriteInput) -> FavouriteInput:
        if self.repository.offer_saved_by_user(data.user_id, data.offer_id):
            raise HTTPException(status_code=400, detail="Offer already saved")

        favourite = self.repository.create(data)
        return FavouriteInput(**favourite.__dict__)

    def delete(self, _id: UUID4) -> bool:
        if not self.repository.favourite_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Favourite not found")
        return self.repository.delete(_id)

    def get_all_by_user(self, user_id: UUID4) -> FavouriteListOutput:
        favourites = self.repository.get_all_by_user(user_id)

        results = []
        for favourite in favourites:
            result = self.repository_offer.get_details(favourite.offer_id)
            results.append(result)

        return FavouriteListOutput(offers=results)
