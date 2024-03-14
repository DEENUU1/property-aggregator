from typing import Optional, Type

from pydantic import UUID4
from sqlalchemy.orm import Session

from models.photo import Photo
from schemas.photo import PhotoInput


class PhotoRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, data: PhotoInput) -> PhotoInput:
        photo = Photo(**data.model_dump(exclude_none=True))
        self.session.add(photo)
        self.session.commit()
        self.session.refresh(photo)
        return PhotoInput(**photo.__dict__)

    def photo_exists_by_url(self, url: str) -> bool:
        photo = self.session.query(Photo).filter_by(url=url).first()
        if photo:
            return True
        return False

    def get_by_id(self, id: UUID4) -> Type[Photo]:
        return self.session.query(Photo).filter_by(id=id).first()

    def delete(self, photo: Type[Photo]) -> bool:
        self.session.delete(photo)
        self.session.commit()
        return True
