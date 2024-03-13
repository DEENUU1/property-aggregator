from sqlalchemy.orm import Session
from models.user import User
from typing import Type


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user(self, username: str) -> Type[User]:
        return self.session.query(User).filter(User.username == username).first()
