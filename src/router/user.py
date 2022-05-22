from unittest import result
from fastapi import APIRouter, Response, Header
from fastapi.responses import JSONResponse 
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from src.schema.user import User
from src.schema.userAuth import UserAuth
from src.db.db import engine
from src.model.user import users
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List
from src.functions_jwt import write_token, validate_token

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
def user_login(data_user: UserAuth):
  with engine.connect() as conn:
    result = conn.execute(users.select().where(users.c.email == data_user.email)).first()
    print(result)
    if result != None:
      check_passw = check_password_hash(result[12], data_user.password)

      if check_passw:
        return {
          "status": 200,
          "message": "Access success"
        }

    return  {
      "status": HTTP_401_UNAUTHORIZED,
      "message": "Access denied"
    }

@user.post("user/login/token")
def user_login_token(user : UserAuth):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.email == user.email)).first()

        if result != None:
            check_passw = check_password_hash(result[12], user.password)
            if check_passw:
                print(user.dict())
                return write_token(user.dict())
            else:
                return Response(status_code=HTTP_401_UNAUTHORIZED)
        else:
            return JSONResponse(content={"message": "User not found"}, status_code=404)

@user.post("/verify/token")
def verify_token(Authorization:  str = Header(None)):
    token = Authorization.split(' ')[1]
    return validate_token(token, output=True)

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