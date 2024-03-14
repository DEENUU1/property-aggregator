from fastapi import APIRouter, Depends
from services.user_service import UserService
from config.database import get_db
from sqlalchemy.orm import Session
from schemas.user import UserIn
from fastapi.security import OAuth2PasswordRequestForm
from auth.auth import get_current_user


router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/register", status_code=201)
def register(data: UserIn, session: Session = Depends(get_db)):
    _service = UserService(session)
    return _service.create(data)


@router.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    _service = UserService(session)
    return _service.login(data)


@router.get("/me", status_code=200)
def me(user: UserIn = Depends(get_current_user)):
    return user
