from typing import List, Dict, Any, Optional

from pydantic import BaseModel, UUID4


class FavouriteInput(BaseModel):
    offer_id: UUID4
    # user_id is set to None, and it's defined as Optional
    # because user_id is assigned on the app site not from client
    user_id: Optional[UUID4] = None


class FavouriteInDb(BaseModel):
    id: UUID4
    offer_id: UUID4
    user_id: UUID4

    class Config:
        orm_mode = True


class FavouriteOutput(BaseModel):
    id: UUID4
    offer_id: UUID4


class FavouriteOfferOutput(BaseModel):
    id: UUID4
    offer: Dict[str, Any]
