from typing import List

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from repositories.favourite_repository import FavouriteRepository
from repositories.offer_repository import OfferRepository
from schemas.favourite import FavouriteInput, FavouriteOfferOutput
from services.user_service import UserService


class FavouriteService:
    """
    Service class for handling user favourites.
    """

    def __init__(self, session: Session):
        """
        Initialize the service.

        Args:
            session (Session): Database session.
        """
        self.repository = FavouriteRepository(session)
        self.repository_offer = OfferRepository(session)
        self.user_service = UserService(session)

    def create(self, data: FavouriteInput) -> FavouriteInput:
        """
        Create a new favourite.

        Args:
            data (FavouriteInput): Details of the favourite to be created.

        Returns:
            FavouriteInput: Details of the created favourite.
        """
        if self.repository.offer_saved_by_user(data.user_id, data.offer_id):
            raise HTTPException(status_code=400, detail="Offer already saved")

        if not self.repository_offer.offer_exists_by_id(data.offer_id):
            raise HTTPException(status_code=404, detail="Offer not found")

        favourite = self.repository.create(data)
        return FavouriteInput(**favourite.__dict__)

    def delete(self, _id: UUID4, user_id: UUID4) -> bool:
        """
        Delete a favourite.

        Args:
            _id (UUID4): ID of the favourite to be deleted.
            user_id (UUID4): ID of the user performing the action.

        Returns:
            bool: True if deletion is successful, False otherwise.
        """
        if not self.repository.favourite_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Favourite not found")

        favourite = self.repository.get_favourite(_id)

        if favourite.user_id != user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        return self.repository.delete(favourite)

    def get_all_by_user(self, user_id: UUID4) -> List[FavouriteOfferOutput]:
        """
        Retrieve all favourites of a user.

        Args:
            user_id (UUID4): ID of the user.

        Returns:
            List[FavouriteOfferOutput]: List of favourite offers of the user.
        """
        favourites = self.repository.get_all_by_user(user_id)

        results = []
        for favourite in favourites:
            result = self.repository_offer.get_details(favourite.offer_id)
            favourite_offer = FavouriteOfferOutput(id=favourite.id, offer=result)
            results.append(favourite_offer)

        return results
