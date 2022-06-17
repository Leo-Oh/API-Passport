from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    id: Optional[int]
    curp: str
    email: EmailStr
    password: str
