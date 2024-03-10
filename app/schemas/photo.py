from pydantic import BaseModel, UUID


class PhotoInput(BaseModel):
    url: str
    offer_id: UUID


class PhotoOutput(BaseModel):
    id: UUID
    url: str
    offer_id: UUID
