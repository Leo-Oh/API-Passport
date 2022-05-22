from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: Optional[int]
    id_user: int
    state: str
    office: str
    curp: str
    office_paperwork: str
    identification_document: str
    identification_document_url: str
    nationality_document: str
    nationality_document_url: str
