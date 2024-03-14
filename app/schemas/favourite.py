from typing import List, Dict, Any, Optional

from pydantic import BaseModel, UUID4


class FavouriteInput(BaseModel):
    offer_id: UUID4
    user_id: Optional[UUID4] = None


class FavouriteOutput(BaseModel):
    offer_id: UUID4


class FavouriteListOutput(BaseModel):
    offers: List[Dict[str, Any]]
