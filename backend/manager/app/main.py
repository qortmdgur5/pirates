from fastapi import FastAPI, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from .oauth import oauth
from .db import crud, database
from .utils import schemas

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


# 회원가입
@app.post("/signup/")
async def signup(user: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_user(db=db, user=user)

# 로그인
@app.post("/login/")
async def login(user: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.authenticate_user(db=db, user=user)

@app.get("/auth/google")
async def google_login(request: Request):
    redirect_uri = request.url_for('google_auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/google/callback")
async def google_auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)
    return {"email": user_info['email']}

@app.get("/auth/kakao")
async def kakao_login(request: Request):
    redirect_uri = request.url_for('kakao_auth')
    return await oauth.kakao.authorize_redirect(request, redirect_uri)

@app.get("/auth/kakao/callback")
async def kakao_auth(request: Request):
    token = await oauth.kakao.authorize_access_token(request)
    user_info = token.get('profile')
    return {"nickname": user_info['nickname']}


# 파티방 관리

# 조 관리

# 매니저 관리

# 프로그램 실행 
