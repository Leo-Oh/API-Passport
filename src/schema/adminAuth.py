from pydantic import BaseModel, EmailStr
from typing import Optional

class AdminAuth(BaseModel):
    registration_tag: Optional[str]
    email : Optional[EmailStr]
    password: str
    
