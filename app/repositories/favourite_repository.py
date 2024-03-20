from typing import Type, List

from pydantic import UUID4
from sqlalchemy.orm import Session

from models.favourite import Favorite
from schemas.favourite import FavouriteInput, FavouriteOutput, FavouriteInDb


class FavouriteRepository:
    """
    Repository class for handling favourites.
    """

    def __init__(self, session: Session):
        """
        Initialize the repository with a database session.

        Args:
            session (Session): The database session.
        """
        self.session = session

    def create(self, data: FavouriteInput) -> FavouriteInDb:
        """
        Create a new favourite.

        Args:
            data (FavouriteInput): The favourite data.

        Returns:
            FavouriteInDb: The created favourite.
        """
        favourite = Favorite(**data.model_dump(exclude_none=True))
        self.session.add(favourite)
        self.session.commit()
        self.session.refresh(favourite)
        return FavouriteInDb(**favourite.__dict__)

    def favourite_exists_by_id(self, _id: UUID4) -> bool:
        """
        Check if a favourite exists by ID.

        Args:
            _id (UUID4): The favourite ID.

        Returns:
            bool: True if the favourite exists, False otherwise.
        """
        favourite = self.session.query(Favorite).filter_by(id=_id).first()
        return bool(favourite)

    def get_favourite(self, _id: UUID4) -> Type[Favorite]:
        """
        Get a favourite by ID.

        Args:
            _id (UUID4): The favourite ID.

        Returns:
            Type[Favorite]: The favourite instance.
        """
        return self.session.query(Favorite).filter_by(id=_id).first()

    def get_all_by_user(self, user_id: UUID4) -> List[FavouriteOutput]:
        """
        Get all favourites by user.

        Args:
            user_id (UUID4): The user ID.

        Returns:
            List[FavouriteOutput]: A list of favourite outputs.
        """
        favourites = self.session.query(Favorite).filter_by(user_id=user_id).all()
        return [FavouriteOutput(**favourite.__dict__) for favourite in favourites]

    def offer_saved_by_user(self, user_id: UUID4, offer_id: UUID4) -> bool:
        """
        Check if an offer is saved by a user.

        Args:
            user_id (UUID4): The user ID.
            offer_id (UUID4): The offer ID.

        Returns:
            bool: True if the offer is saved, False otherwise.
        """
        favourite = self.session.query(Favorite).filter(Favorite.offer_id == offer_id).filter(
            Favorite.user_id == user_id
        ).first()
        return bool(favourite)

    def delete(self, favourite: Type[Favorite]) -> bool:
        """
        Delete a favourite.

        Args:
            favourite (Type[Favorite]): The favourite instance.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        self.session.delete(favourite)
        self.session.commit()
        return True
