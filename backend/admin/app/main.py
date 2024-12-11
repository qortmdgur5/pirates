import logging
import time
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from .db import database, errorLog
from .utils import utils
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from .routers import admin, owner, manager, user
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

config = utils.load_config("config.yaml")
app.add_middleware(SessionMiddleware, secret_key=config['SECRET_KEY'])

app.include_router(admin.router)
app.include_router(owner.router)
app.include_router(manager.router)
app.include_router(user.router)

logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(message)s")

class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next, db: AsyncSession = Depends(database.get_db)):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logging.error(f"Unhandled exception: {str(e)}")
            await errorLog.log_error(db, str(e)) 
            return JSONResponse(
                status_code=500, content={"msg": "Internal server error"}
            )

app.add_middleware(ExceptionMiddleware)

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logging.info(f"Request {request.url.path} took {process_time:.4f} seconds")
    return response

