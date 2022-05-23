from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from os import getcwd, remove
from shutil import rmtree
import uuid


document_nationality = APIRouter()

@document_nationality.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    #with open(getcwd() + "/src/uploads/nationality/" + file.filename, "wb") as myfile:
   
    id_image = uuid.uuid4()
    with open(getcwd() + "/src/uploads/nationality/" + str(id_image)+".jpg", "wb") as myfile:
        content = await file.read()
        myfile.write(content)
        myfile.close()
    return JSONResponse(content={
            "message": "File saved",
            "url": myfile.name
        }, status_code=200)

@document_nationality.get("/file/{name_file}")
def get_file(name_file: str):
    return FileResponse(getcwd() + "/src/uploads/nationality/" + name_file)

@document_nationality.get("/download/{name_file}")
def download_file(name_file: str):
    return FileResponse(getcwd() + "/src/uploads/nationality/" + name_file, media_type="application/octet-stream", filename=name_file)

@document_nationality.delete("/delete/{name_file}")
def delete_file(name_file: str):
    try:
        remove(getcwd() + "/src/uploads/nationality/" + name_file)
        return JSONResponse(content={
            "removed": True
        }, status_code=200)
    except FileNotFoundError:
        return JSONResponse(content={
            "removed": False,
            "message": "File not found"
        }, status_code=404)