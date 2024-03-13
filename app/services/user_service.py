from typing import Type

from sqlalchemy.orm import Session

from models.user import User
from repositories.user_repository import UserRepository


class UserService:

    def __init__(self, session: Session):
        self.repository = UserRepository(session)

    def get_user(self, username: str) -> Type[User]:
        return self.repository.get_user(username)
