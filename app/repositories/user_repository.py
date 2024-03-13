from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserIn


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: UserIn, hashed_password: str):
        db_user = User(**data.model_dump(exclude={"password"}), hashed_password=hashed_password)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def user_exists_by_email(self, email: str) -> bool:
        return self.session.query(User).filter(User.email == email).first() is not None

    def user_exists_by_username(self, username: str) -> bool:
        return self.session.query(User).filter(User.username == username).first() is not None

    def get_user_by_email(self, email: str):
        return self.session.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str):
        return self.session.query(User).filter(User.username == username).first()
