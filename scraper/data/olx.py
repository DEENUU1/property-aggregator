from typing import Optional, Annotated, Any

from pydantic import BaseModel, BeforeValidator, Field, Json

PyObjectId = Annotated[str, BeforeValidator(str)]


class Olx(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    category: str
    sub_category: int
    data: Json[Any]
    parsed: bool = False
    send: bool = False
