import logging
import os
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .db import database, errorLog
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from .routers import admin, owner, manager, user
from dotenv import load_dotenv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.include_router(admin.router)
app.include_router(owner.router)
app.include_router(manager.router)
app.include_router(user.router)

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Unhandled exception: {str(e)}")
            return JSONResponse(status_code=500, content={"msg": "Internal server error"})


app.add_middleware(ExceptionMiddleware)

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    if process_time > 1: 
        logging.warning(f"Request {request.url.path} took {process_time:.4f} seconds")
    return response

