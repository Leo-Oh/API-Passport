from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from src.router.user import user
from src.router.admin import admin
from src.router.document_identification import document_identification
from src.router.document_nationality import document_nationality
from src.router.appointment import appointment
from src.documentation.doc import tags_metadatas
import uvicorn

app = FastAPI(
    title="REST API to passport system",
    description="By ISW UV",
    version="0.3",
    openapi_tags=tags_metadatas
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user, prefix='/api',tags=["User"])
app.include_router(admin, prefix='/api/mode',tags=["Admin"])
app.include_router(document_identification, prefix='/api/documents/identification',tags=["Documents Identification"])
app.include_router(document_nationality, prefix='/api/documents/nationality',tags=["Documents Nationality"])
app.include_router(appointment, prefix='/api',tags=["Appointment"])
load_dotenv()

if __name__ == "__main__":
    uvicorn.run(app, port=9090, host="0.0.0.0")