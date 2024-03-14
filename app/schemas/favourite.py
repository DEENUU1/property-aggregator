from pydantic import BaseModel, UUID4
from typing import List, Optional


class FavouriteInput(BaseModel):
    user_id: UUID4
    offer_id: UUID4

