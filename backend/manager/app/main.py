from fastapi import FastAPI, Depends, Request, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession
from .oauth import oauth
from .db import crud, database
from .utils import schemas

app = FastAPI()

# 회원가입
@app.post("/signup/", summary="회원가입", tags=["signup"])
async def signup(user: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_user(db=db, user=user)





# 로그인
@app.post("/login/", summary="login", tags=["login"])
async def login(user: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.authenticate_user(db=db, user=user)

@app.get("/auth/google", summary="구글 로그인", tags=["login"])
async def google_login(request: Request):
    redirect_uri = request.url_for('google_auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/google/callback", summary="구글 로그인 권한", tags=["login"])
async def google_auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)
    return {"email": user_info['email']}

@app.get("/auth/kakao", summary="카카오 로그인", tags=["login"])
async def kakao_login(request: Request):
    redirect_uri = request.url_for('kakao_auth')
    return await oauth.kakao.authorize_redirect(request, redirect_uri)

@app.get("/auth/kakao/callback", summary="카카오 로그인 권한", tags=["login"])
async def kakao_auth(request: Request):
    token = await oauth.kakao.authorize_access_token(request)
    user_info = token.get('profile')
    return {"nickname": user_info['nickname']}






# 파티방 관리
@app.post("/company/{companyId}/party", summary="파티방 등록", tags=["party"])
async def create_company_party(
    companyId: int = Path(..., description="회사 ID"), 
    party: schemas.PartyBase = Body(..., description="파티 정보"), 
    db: AsyncSession = Depends(database.get_db)
    ):
    """
    파티방 등록.

    - **accommodation_id**: 숙소 pk.
    - **partyDate**: 파티 날짜.
    - **partyOpen**: 파티 여부.
    - **partyTime**: 파티 시작 시간.
    - **number**: 파티 참석 인원.
    - **partyOn**: 파티방 ON/OFF.
    """
    
    return await crud.create_party(db=db, party=party)
# 조 관리

# 매니저 관리

# 프로그램 실행 
