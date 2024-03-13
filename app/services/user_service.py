from datetime import timedelta

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth.security import get_password_hash
from auth.security import pwd_context, create_access_token
from config.settings import settings
from repositories.user_repository import UserRepository
from schemas.user import UserIn


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

    def login(self, data: OAuth2PasswordRequestForm):
        user = self.repository.get_user_by_username(data.username)
        if not user or not pwd_context.verify(data.password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
