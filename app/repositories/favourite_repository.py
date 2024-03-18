from sqlalchemy.orm import Session
from schemas.favourite import FavouriteInput, FavouriteOutput, FavouriteInDb
from models.favourite import Favorite
from typing import Type, List
from pydantic import UUID4


class FavouriteRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, data: FavouriteInput) -> FavouriteInDb:
        favourite = Favorite(**data.model_dump(exclude_none=True))
        self.session.add(favourite)
        self.session.commit()
        self.session.refresh(favourite)
        return FavouriteInDb(**favourite.__dict__)

    def favourite_exists_by_id(self, _id: UUID4) -> bool:
        favourite = self.session.query(Favorite).filter_by(id=_id).first()
        if favourite:
            return True
        return False

    def get_favourite(self, _id: UUID4) -> Type[Favorite]:
        return self.session.query(Favorite).filter_by(id=_id).first()

    def get_all_by_user(self, user_id: UUID4) -> List[FavouriteOutput]:
        favourites = self.session.query(Favorite).filter_by(user_id=user_id).all()
        return [FavouriteOutput(**favourite.__dict__) for favourite in favourites]

    def offer_saved_by_user(self, user_id: UUID4, offer_id: UUID4) -> bool:
        favourite = self.session.query(Favorite).filter(Favorite.offer_id == offer_id).filter(Favorite.user_id == user_id).first()
        if favourite:
            return True
        else:
            return False

    def delete(self, favourite: Type[Favorite]) -> bool:
        self.session.delete(favourite)
        self.session.commit()
        return True
