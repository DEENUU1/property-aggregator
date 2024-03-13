from typing import Type
from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.user import User
from repositories.user_repository import UserRepository
from schemas.user import UserIn
from auth.security import get_password_hash


class UserService:

    def __init__(self, session: Session):
        self.repository = UserRepository(session)

    def create(self, data: UserIn):
        if self.repository.user_exists_by_email(data.email):
            raise HTTPException(status_code=400, detail="Username already registered")
        if self.repository.user_exists_by_username(data.username):
            raise HTTPException(status_code=400, detail="Username already registered")

        hashed_password = get_password_hash(data.password)
        user = self.repository.create(data, hashed_password)
        return user

