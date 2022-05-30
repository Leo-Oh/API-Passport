from pydantic import BaseModel
from datetime import date, datetime, time, timedelta
from typing import Optional

class Appointment(BaseModel):
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
    date: date
    time: time
    status: bool
