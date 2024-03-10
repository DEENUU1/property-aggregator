from pydantic import BaseModel, UUID4


class PhotoInput(BaseModel):
    url: str
    offer_id: UUID4


class PhotoOutput(BaseModel):
    id: UUID4
    url: str
    offer_id: UUID4
