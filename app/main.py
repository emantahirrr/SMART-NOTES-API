from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from app.routers import ai_router, users_router, notes_router 
from app.db import create_db_and_tables
load_dotenv()
app = FastAPI()
app.include_router(ai_router)
app.include_router(users_router)
app.include_router(notes_router)
@app.get("/")
def read_root():
    return {"message": "Smart Notes API is running with Groq!"}
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "An unexpected error occurred. Please try again later."},
    )
@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "healthy"}
