from fastapi import APIRouter, Depends
from services.user_service import UserService
from config.database import get_db
from sqlalchemy.orm import Session
from schemas.user import UserIn, UserInDBBase
from fastapi.security import OAuth2PasswordRequestForm
from auth.auth import get_current_user


router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/register", status_code=201, response_model=UserInDBBase)
def register(data: UserIn, session: Session = Depends(get_db)):
    _service = UserService(session)
    return _service.create(data)


@router.post("/login", status_code=201)
def login(data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    _service = UserService(session)
    return _service.login(data)


@router.get("/me", status_code=200)
def get_me(user: UserIn = Depends(get_current_user)):
    return user


@router.delete("/me", status_code=204)
def delete_me(
        user: UserIn = Depends(get_current_user),
        session: Session = Depends(get_db)
):
    _service = UserService(session)
    return _service.delete_user(user.id)
