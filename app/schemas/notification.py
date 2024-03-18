from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, UUID4


class NotificationInput(BaseModel):
    user_id: Optional[UUID4] = None
    title: Optional[str] = None
    message: Optional[str] = None


class NotificationOutput(BaseModel):
    id: UUID4
    title: Optional[str] = None
    message: Optional[str] = None
    created_at: datetime
    read: bool = False
    offers: List[Dict[str, Any]] = None
    user_id: UUID4
