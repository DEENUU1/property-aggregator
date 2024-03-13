from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    email: str
    username: str
    is_superuser: bool = False
    is_active: bool = True


class UserIn(UserBase):
    password: str


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    hashed_password: str


class TokenData(BaseModel):
    username: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
