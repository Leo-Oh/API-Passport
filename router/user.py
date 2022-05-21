from unittest import result
from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from schema.user import User, UserLogin
from db.db import engine
from model.user import users
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List


user = APIRouter()


@user.get("/user", response_model=List[User])
def get_users():
  with engine.connect() as conn:
    result = conn.execute(users.select()).fetchall() 

    return result


@user.get("/user/{user_id}", response_model=User)
def get_user(user_id: str):
  with engine.connect() as conn:
    result = conn.execute(users.select().where(users.c.id == user_id)).first()

    return result



@user.post("/user", status_code=HTTP_201_CREATED)
def create_user(data_user: User):
  with engine.connect() as conn:
    
    result = conn.execute(users.select().where(users.c.email == data_user.email)).first()
    if result != None:
       return Response(status_code=HTTP_401_UNAUTHORIZED)
    
    new_user = data_user.dict()
    new_user["password"] = generate_password_hash(data_user.password, "pbkdf2:sha256:30", 30)

    conn.execute(users.insert().values(new_user))

    return Response(status_code=HTTP_201_CREATED)


@user.post("/user/login", status_code=200)
def user_login(data_user: UserLogin):
  with engine.connect() as conn:
    result = conn.execute(users.select().where(users.c.email == data_user.email)).first()

    if result != None:
      check_passw = check_password_hash(result[3], data_user.password)

      if check_passw:
        return {
          "status": 200,
          "message": "Access success"
        }

    return  {
      "status": HTTP_401_UNAUTHORIZED,
      "message": "Access denied"
    }


@user.put("/user/{user_id}}", response_model=User)
def update_user(data_update: User, user_id: str):
  with engine.connect() as conn:
    encryp_passw = generate_password_hash(data_update.password, "pbkdf2:sha256:30", 30)

    conn.execute(users.update().values(
        id = data_update.id,
        country = data_update.country,
        state = data_update.state,
        default_office = data_update.default_office,
        born_country = data_update.born_country,
        nationality = data_update.nationality,
        name = data_update.name,
        first_surname = data_update.first_surname,
        second_surname = data_update.second_surname,
        telephone = data_update.telephone,
        optional_telephone = data_update.optional_telephone,
        email = data_update.email,
        password = encryp_passw

        ).where(users.c.id == user_id))

    result = conn.execute(users.select().where(users.c.id == user_id)).first()

    return result


@user.delete("/api/user/{user_id}", status_code=HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
  with engine.connect() as conn:
    conn.execute(users.delete().where(users.c.id == user_id))

    return Response(status_code=HTTP_204_NO_CONTENT)