from sqlalchemy.orm import Session

from repositories.favourite_repository import FavouriteRepository
from schemas.favourite import FavouriteInput


class FavouriteService:

    def __init__(self, session: Session):
        self.repository = FavouriteRepository(session)

    def create(self, data: FavouriteInput) -> FavouriteInput:
        return self.repository.create(data)
