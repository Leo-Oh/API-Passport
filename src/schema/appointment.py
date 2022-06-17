from pydantic import BaseModel
from datetime import date, datetime, time, timedelta
from typing import Optional

class Appointment(BaseModel):
    id: Optional[int]
    id_user: int
    curp: str
    name: str
    first_surname: str
    second_surname: str
    born_country: str
    born_date: str
    nationality: str
    address: str
    telephone: str
    optional_telephone: Optional[str]
    state: str
    office: str
    office_paperwork: str
    identification_document: str
    identification_document_url: str
    nationality_document: str
    nationality_document_url: str
    date: date
    time: time
    status: bool
