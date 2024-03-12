from typing import Optional, Annotated

from pydantic import BaseModel, BeforeValidator, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class Otodom(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    category: str
    sub_category: str
    data: str
    parsed: bool = False
    send: bool = False
