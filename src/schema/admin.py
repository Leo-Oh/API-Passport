from pydantic import BaseModel, EmailStr
from typing import Optional


class Admin(BaseModel):
    id: Optional[int]
    name: str
    first_surname: str
    second_surname: str
    telephone: str
    role: str
    registration_tag: str
    email: EmailStr
    password: str
