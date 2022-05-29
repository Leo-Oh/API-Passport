from fastapi import APIRouter, Response, Header
from fastapi.responses import JSONResponse 
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


@appointment.get("/appointments/{name}", response_model=List[Appointment])
def get_all_appointments(name: str):
  with engine.connect() as conn:
    result = conn.execute(appointments.select().where(appointments.c.name == name)).fetchall() 
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



@appointment.delete("/appointment/{id_appointment}", status_code=HTTP_204_NO_CONTENT)
def delete_user(id_appointment: str):
  with engine.connect() as conn:
    conn.execute(appointments.delete().where(appointments.c.id == id_appointment))

    return Response(status_code=HTTP_204_NO_CONTENT)