from sqlalchemy.orm import Session
from schemas.favourite import FavouriteInput
from models.favourite import Favorite


class FavouriteRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, data: FavouriteInput) -> FavouriteInput:
        favourite = Favorite(**data.model_dump(exclude_none=True))
        self.session.add(favourite)
        self.session.commit()
        self.session.refresh(favourite)
        return FavouriteInput(**favourite.__dict__)
