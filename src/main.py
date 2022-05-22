from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from src.router.user import user
from src.documentation.doc import tags_metadatas
import uvicorn

app = FastAPI(
    title="REST API to passport system",
    description="By ISW UV",
    version="0.1",
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
load_dotenv()

if __name__ == "__main__":
    uvicorn.run(app, port=9090, host="0.0.0.0")