from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, UUID4


class NotificationInput(BaseModel):
    # user_id is set by default to None and it's Optional
    # because it's assigned on the app site not from client form
    user_id: Optional[UUID4] = None
    title: Optional[str] = None
    message: Optional[str] = None


class NotificationOutput(BaseModel):
    id: UUID4
    title: Optional[str] = None
    message: Optional[str] = None
    read: bool = False
    created_at: datetime
    user_id: UUID4
    offers: List[Dict[str, Any]] = None
