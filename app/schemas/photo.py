from pydantic import BaseModel


class PhotoInput(BaseModel):
    url: str

