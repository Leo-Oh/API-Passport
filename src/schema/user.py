from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    id: Optional[str]
    country: str
    state: str
    default_office: str
    born_country: str
    nationality: str
    name: str
    first_surname: str
    second_surname: str
    telephone: str
    optional_telephone: Optional[str]
    email: EmailStr
    password: str
