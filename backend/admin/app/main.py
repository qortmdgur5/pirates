import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .utils import utils
from starlette.middleware.sessions import SessionMiddleware
from .routers import admin, owner, manager, user

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


@app.middleware("http")
async def log_request_time(
    request: Request, 
    call_next
    ):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request {request.url.path} took {process_time:.4f} seconds")
    return response

