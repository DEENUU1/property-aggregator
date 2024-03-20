from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from auth import security
from config.database import get_db
from models.user import User
from schemas.user import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db: Session, username: str):
    """
    Retrieve a user from the database by their username.

    Args:
        db (Session): The database session.
        username (str): The username of the user to retrieve.

    Returns:
        User: The user object if found, otherwise None.
    """
    return db.query(User).filter(User.username == username).first()


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    """
    Get the current user based on the provided token.

    Args:
        token (str): The authentication token.
        db (Session): The database session.

    Raises:
        HTTPException: If credentials cannot be validated.

    Returns:
        User: The current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
