from fastapi import APIRouter, Response, Header
from fastapi.responses import JSONResponse 
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from src.schema.admin import Admin
from src.schema.adminAuth import AdminAuth
from src.db.db import engine
from src.model.admin import admins
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List
from src.functions_jwt import write_token, validate_token

admin = APIRouter()


@admin.get("/admin", response_model=List[Admin])
def get_admins():
  with engine.connect() as conn:
    result = conn.execute(admins.select()).fetchall() 
    return result


@admin.get("/admin/{admin_id}", response_model=Admin)
def get_admin(admin_id: int):
  with engine.connect() as conn:
    result = conn.execute(admins.select().where(admins.c.id == admin_id)).first()
  return result


@admin.post("/admin", status_code=HTTP_201_CREATED)
def create_admin(data_admin: Admin):
  with engine.connect() as conn:
    result = conn.execute(admins.select().where(admins.c.email == data_admin.email or admins.c.registration_tag == data_admin.registration_tag)).first()
    if result != None:
       return Response(status_code=HTTP_401_UNAUTHORIZED)
    
    new_admin = data_admin.dict()
    new_admin["password"] = generate_password_hash(data_admin.password, "pbkdf2:sha256:30", 30)

    conn.execute(admins.insert().values(new_admin))

    return Response(status_code=HTTP_201_CREATED)




#@admin.post("/admin/login", status_code=200)
#def admin_login(data_admin: AdminAuth):
#  with engine.connect() as conn:
#    if(data_admin.email != None):
#      result = conn.execute(admins.select().where(admins.c.email == data_admin.email )).first()
#    if(data_admin.registration_tag != None):
#      result = conn.execute(admins.select().where(admins.c.registration_tag == data_admin.registration_tag )).first()
#
#    if result != None:
#      check_passw = check_password_hash(result[8], data_admin.password)
#      if check_passw:
#        return {
#          "status": 200,
#          "message": "Access success",
#          "user" : result
#        }
#      else:
#        return Response(status_code=HTTP_401_UNAUTHORIZED)
#    return JSONResponse(content={"message": "User not found"}, status_code=404)

@admin.post("/admin/login/token")
def admin_login_token(admin : AdminAuth):
  with engine.connect() as conn:
    if(admin.email != None):
      result = conn.execute(admins.select().where(admins.c.email == admin.email )).first()
    if(admin.registration_tag != None):
      result = conn.execute(admins.select().where(admins.c.registration_tag == admin.registration_tag )).first()

    if result != None:
      check_passw = check_password_hash(result[8], admin.password)
      if check_passw:
        return {
          "status": 200,
          "message": "Access success",
          "token" : write_token(admin.dict()),
          "user" : result
        }
      else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
    else:
      return JSONResponse(content={"message": "User not found"}, status_code=404)

@admin.post("/admin/verify/token")
def verify_token(user_token:str=Header(default=None)):
  #token = user_token.split(' ')[1]
  token=user_token.split(" ")[0]
  return validate_token(token, output=True)

@admin.put("/admin/{admin_id}", response_model=Admin)
def update_admin(data_update: Admin, admin_id: int):
  with engine.connect() as conn:
    encryp_passw = generate_password_hash(data_update.password, "pbkdf2:sha256:30", 30)

    conn.execute(admins.update().values(
        id = data_update.id,
        name = data_update.name,
        first_surname = data_update.first_surname,
        second_surname = data_update.second_surname,
        telephone = data_update.telephone,
        role = data_update.role,
        registration_tag = data_update.registration_tag,
        email = data_update.email,
        password = encryp_passw

        ).where(admins.c.id == admin_id))

    result = conn.execute(admins.select().where(admins.c.id == admin_id)).first()

    return result


@admin.delete("/admin/{admin_id}", status_code=HTTP_204_NO_CONTENT)
def delete_admin(admin_id: int):
  with engine.connect() as conn:
    conn.execute(admins.delete().where(admins.c.id == admin_id))
    return Response(status_code=HTTP_204_NO_CONTENT)