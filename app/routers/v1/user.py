from fastapi import APIRouter, Depends
from services.user_service import UserService
from config.database import get_db
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from config.settings import settings
from schemas.user import TokenData, UserIn

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/register")
def register(data: UserIn, session: Session = Depends(get_db)):
    _service = UserService(session)
    return _service.create(data)

