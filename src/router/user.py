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


@user.get("/users", response_model=List[User])
def get_users():
  with engine.connect() as conn:
    result = conn.execute(users.select()).fetchall() 

    return result


@user.get("/user/{user_id}", response_model=User)
def get_user(user_id: int):
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




#@user.post("/user/login", status_code=200)
#def user_login(data_user: UserAuth):
#  with engine.connect() as conn:
#    result = conn.execute(users.select().where(users.c.email == data_user.email)).first()
#    if result != None:
#      check_passw = check_password_hash(result[12], data_user.password)
#      if check_passw:
#        return {
#          "status": 200,
#          "message": "Access success",
#          "user" : result
#        }
#      else:
#        return Response(status_code=HTTP_401_UNAUTHORIZED)
#
#    return JSONResponse(content={"message": "User not found"}, status_code=404)

@user.post("/user/login/token")
def user_login_token(user : UserAuth):
  with engine.connect() as conn:
    result = conn.execute(users.select().where(users.c.email == user.email)).first()
    if result != None:
        check_passw = check_password_hash(result[3], user.password)
        if check_passw:
            return {
              "status": 200,
              "message": "Access success",
              "token" : write_token(user.dict()),
              "user" : result
            }
        else:
            return Response(status_code=HTTP_401_UNAUTHORIZED)
    else:
        return JSONResponse(content={"message": "User not found"}, status_code=404)

@user.post("/user/verify/token")
def verify_token(user_token:str=Header(default=None)):
  #token = user_token.split(' ')[1]
  token=user_token.split(" ")[0]
  return validate_token(token, output=True)
  
@user.put("/user/{user_id}", response_model=User)
def update_user(data_update: User, user_id: str):
  with engine.connect() as conn:
    encryp_passw = generate_password_hash(data_update.password, "pbkdf2:sha256:30", 30)

    conn.execute(users.update().values(
        id = data_update.id,
        curp = data_update.curp,
        email = data_update.email,
        password = encryp_passw

        ).where(users.c.id == user_id))

    result = conn.execute(users.select().where(users.c.id == user_id)).first()

    return result


@user.delete("/user/{user_id}", status_code=HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
  with engine.connect() as conn:
    conn.execute(users.delete().where(users.c.id == user_id))

    return Response(status_code=HTTP_204_NO_CONTENT)