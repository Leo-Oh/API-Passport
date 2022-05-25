from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from os import getcwd, remove
from shutil import rmtree
import uuid


document_identification = APIRouter()

@document_identification.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    #with open(getcwd() + "/src/uploads/identification" + file.filename, "wb") as myfile:
   
    id_image = uuid.uuid4()
    with open(getcwd() + "/src/uploads/identification/" + str(id_image)+".jpg", "wb") as myfile:
    #with open("src/uploads/identification/" + str(id_image)+".jpg", "wb") as myfile:
        content = await file.read()
        myfile.write(content)
        myfile.close()
    return JSONResponse(content={
            "message": "File saved",
            "url": myfile.name
        }, status_code=200)

@document_identification.get("/file/{name_file}")
def get_file(name_file: str):
    #return FileResponse(getcwd() + "/src/uploads/identification/" + name_file)
    return FileResponse("src/uploads/identification/" + name_file)


@document_identification.get("/download/{name_file}")
def download_file(name_file: str):
    #return FileResponse(getcwd() + "/src/uploads/identification/" + name_file, media_type="application/octet-stream", filename=name_file)
    return FileResponse("src/uploads/identification/" + name_file, media_type="application/octet-stream", filename=name_file)


@document_identification.delete("/delete/{name_file}")
def delete_file(name_file: str):
    try:
        #remove(getcwd() + "/src/uploads/identification/" + name_file)
        remove("src/uploads/identification/" + name_file)
        return JSONResponse(content={
            "removed": True
        }, status_code=200)
    except FileNotFoundError:
        return JSONResponse(content={
            "removed": False,
            "message": "File not found"
        }, status_code=404)