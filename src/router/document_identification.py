from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from os import getcwd, remove
from shutil import rmtree
import uuid

import pytesseract
import json



document_identification = APIRouter()


def token(string):
    start, i = 0, 0
    token_list = []
    for x in range(0, len(string)):
        if " " == string[i:i+1]:
            token_list.append(string[start:i])
            start = i + 1
        i += 1
    token_list.append(string[start:i])
    return token_list

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def num_there(s):
    return any(i.isdigit() for i in s)


@document_identification.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    #with open(getcwd() + "/src/uploads/identification" + file.filename, "wb") as myfile:

    if(file.filename[-4:] == ".jpg" or file.filename[-4:] == ".png" or file.filename[-5:] == ".jpeg"):
        id_image = uuid.uuid4()
        
        with open(getcwd() + "/src/uploads/identification/" + str(id_image)+".jpg", "wb") as myfile:
            content = await file.read()
            myfile.write(content)
            myfile.close()
       
            TextIOWrapper = pytesseract.image_to_string(myfile.name)

            data = token(TextIOWrapper)
            calle = find_between( TextIOWrapper, "C ", "COL" )
            colonia = find_between( TextIOWrapper, "COL ", "ORIZABA")
            colonia = find_between( TextIOWrapper, "COL ", "CORDOBA")
            fecha = ""
            curp = ""

            for i in data:  
              if len(i) == 18 and i[-1].isdigit():      
                  curp = i
              if "/" in i and num_there(i) == True:
                fecha = i

            fecha = fecha[0:10:1]
            primer_apellido = find_between( TextIOWrapper, "NACIMIENTO", fecha)
            segundo_apellido = find_between( TextIOWrapper, fecha, "sex")
            nombres = find_between( TextIOWrapper, "H", "DOMICILIO")
            nombres = find_between( TextIOWrapper, "M", "DOMICILIO")
            nombres = find_between( TextIOWrapper, "sex", "DOMICILIO")

            information = {
              "name": nombres.strip('\n'),
              "first_surname": primer_apellido.strip('\n'),
              "second_surname": segundo_apellido.strip('\n'),
              "street": calle.strip('\n'),
              "suburb": colonia.strip('\n'),
              "curp": curp.strip('\n'),
              "date_birth": fecha.strip('\n') 
            }
            json_informacion = json.dumps(information)
        return JSONResponse(content={
            "message": "File saved",
            "url": myfile.name,
            "image_information": information
            }, status_code=200)
    else:
        return JSONResponse(content={
            "message": "File not saved, verify",
            }, status_code=400)

    

@document_identification.get("/file/{name_file}")
def get_file(name_file: str):

    ruta_imagen = getcwd() + "/src/uploads/identification/" + name_file

    TextIOWrapper = pytesseract.image_to_string(ruta_imagen)
    data = token(TextIOWrapper)
    calle = find_between( TextIOWrapper, "C ", "COL" )
    colonia = find_between( TextIOWrapper, "COL ", "ORIZABA")
    colonia = find_between( TextIOWrapper, "COL ", "CORDOBA")
    fecha = ""
    curp = ""

    for i in data:  
      if len(i) == 18 and i[-1].isdigit():      
          curp = i
      if "/" in i and num_there(i) == True:
        fecha = i

    fecha = fecha[0:10:1]
    primer_apellido = find_between( TextIOWrapper, "NACIMIENTO", fecha)
    segundo_apellido = find_between( TextIOWrapper, fecha, "sex")
    nombres = find_between( TextIOWrapper, "H", "DOMICILIO")
    nombres = find_between( TextIOWrapper, "M", "DOMICILIO")
    nombres = find_between( TextIOWrapper, "sex", "DOMICILIO")

    information = {
      "name": nombres.strip('\n'),
      "first_surname": primer_apellido.strip('\n'),
      "second_surname": segundo_apellido.strip('\n'),
      "street": calle.strip('\n'),
      "suburb": colonia.strip('\n'),
      "curp": curp.strip('\n'),
      "date_birth": fecha.strip('\n') 
    }
    json_informacion = json.dumps(information)
    return JSONResponse(content={
        "message": "File found",
        "url": ruta_imagen,
        "image_information": information
        }, status_code=200)
   
    #return FileResponse(getcwd() + "/src/uploads/identification/" + name_file)


@document_identification.get("/download/{name_file}")
def download_file(name_file: str):
    return FileResponse(getcwd() + "/src/uploads/identification/" + name_file, media_type="application/octet-stream", filename=name_file)

@document_identification.delete("/delete/{name_file}")
def delete_file(name_file: str):
    try:
        remove(getcwd() + "/src/uploads/identification/" + name_file)
        return JSONResponse(content={
            "removed": True
        }, status_code=200)
    except FileNotFoundError:
        return JSONResponse(content={
            "removed": False,
            "message": "File not found"
        }, status_code=404)