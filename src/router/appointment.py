from fastapi import APIRouter, Response, Header
from fastapi.responses import JSONResponse
from sqlalchemy import true 
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from src.schema.appointment import Appointment
from src.db.db import engine
from src.model.appointment import appointments
from typing import List

appointment = APIRouter()

"""
==================================================
    Returns a list of Appointments of all users
==================================================
"""
@appointment.get("/appointments", response_model=List[Appointment])
def get_all_appointments():
  with engine.connect() as conn:
    result = conn.execute(appointments.select()).fetchall() 
    return result

"""
==================================================
      Returns a list of Appointments of 
        all users with status are true
==================================================
"""
@appointment.get("/appointments/status_true", response_model=List[Appointment])
def get_all_appointments_with_status_true():
  with engine.connect() as conn:
    result = conn.execute(appointments.select().where(appointments.c.status == True)).fetchall() 
    return result


"""
==================================================
      Returns a list of Appointments of 
        all users with status are false
==================================================
"""
@appointment.get("/appointments/status_false", response_model=List[Appointment])
def get_all_appointments_with_status_false():
  with engine.connect() as conn:
    result = conn.execute(appointments.select().where(appointments.c.status == False)).fetchall() 
    return result


"""
==================================================
            Returns a list of Appointments 
                based on the user ID
==================================================
"""
@appointment.get("/appointments/{id_user}", response_model=List[Appointment])
def get_all_appointments_by_user_id(id_user: int):
  with engine.connect() as conn:
    result = conn.execute(appointments.select().where(appointments.c.id_user == id_user)).fetchall() 
    return result

"""
==================================================
    Returns a Appointment by ID 
==================================================
"""
@appointment.get("/appointment/{id_appointment}", response_model=Appointment)
def get_appointment(id_appointment: int):
  with engine.connect() as conn:
    result = conn.execute(appointments.select().where(appointments.c.id == id_appointment)).first()
  return result

"""
==================================================
          Returns a Appointment based on 
        the user ID and the appointment ID
==================================================
"""
@appointment.get("/appointment/{id_user}/{id_appointment}", response_model=Appointment)
def get_appointment_by_user_id_and_by_appointment_id(id_user: int, id_appointment: int):
  with engine.connect() as conn:
    result = conn.execute(appointments.select().where(appointments.c.id == id_appointment, appointments.c.id_user == id_user )).first()
  return result

@appointment.post("/appointment", status_code=HTTP_201_CREATED)
def create_appointment(data_appointment: Appointment):
  with engine.connect() as conn:
    new_appointment = data_appointment.dict()
    conn.execute(appointments.insert().values(new_appointment))
    return Response(status_code=HTTP_201_CREATED)

@appointment.put("/appointment/{appontment_id}", response_model=Appointment)
def update_appointment(data_update: Appointment, appointment_id: int):
  with engine.connect() as conn:
    conn.execute(appointments.update().values(
      id = data_update.id,
      id_user = data_update.id_user,
      curp = data_update.curp,
      name = data_update.name,
      first_surname = data_update.first_surname,
      second_surname = data_update.second_surname,
      born_country = data_update.born_country,
      born_date = data_update.born_date,
      nationality = data_update.nationality,
      address = data_update.address,
      telephone = data_update.telephone,
      optional_telephone = data_update.optional_telephone,
      state = data_update.state,
      office = data_update.office,
      office_paperwork = data_update.office_paperwork,
      identification_document = data_update.identification_document,
      identification_document_url = data_update.identification_document_url,
      nationality_document = data_update.nationality_document,
      nationality_document_url = data_update.nationality_document_url,
      date = data_update.date,
      time = data_update.time,
      status = data_update.status,
    ).where(appointments.c.id == appointment_id))
    result = conn.execute(appointments.select().where(appointments.c.id == appointment_id)).first()
    return result

@appointment.delete("/appointment/{id_appointment}", status_code=HTTP_204_NO_CONTENT)
def delete_user(id_appointment: str):
  with engine.connect() as conn:
    conn.execute(appointments.delete().where(appointments.c.id == id_appointment))

    return Response(status_code=HTTP_204_NO_CONTENT)