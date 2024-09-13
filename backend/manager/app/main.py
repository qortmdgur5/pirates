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
## 파티방 등록
@app.post("/party", summary="파티방 등록", tags=["party"])
async def create_party(
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


## 날짜별 파티방 리스트
@app.get("/party", response_model=schemas.PartyBase,summary="날짜별 파티방 리스트", tags=["party"])
async def read_party_list(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
    owners = await crud.party_list(db, skip=skip, limit=limit)
    return owners

## 전체 명단 리스트
@app.get("/participant/{partyId}", response_model=schemas.Participant, summary="날짜별 파티방 명단", tags=["party"])
async def read_party_participant(partyId: int, db: AsyncSession = Depends(database.get_db)):
    participant = await crud.party_participant(db, party_id=partyId)
    return participant


## 파티방 명단 생성
@app.post("/participant", response_model=schemas.Participant, summary="파티방 명단 등록", tags=["party"])
async def create_party_participant(participant: schemas.Participant, db: AsyncSession = Depends(database.get_db)):
    """
    파티방 명단 등록.
    
    - **party_id**: 파티 아이디.
    - **name**: 이름.
    - **phone**: 핸드폰.
    - **mbti**: mbti.
    - **age**: 나이.
    - **region**: 지역.
    - **gender**: 성별.
    """
    return await crud.create_party_participant(db=db, participant=participant)

## 파티방 명단 수정
@app.put("/participant/{id}", response_model=schemas.Participant, summary="파티 수정", tags=["party"])
async def update_party_participant(id: int, participant: schemas.Participant, db: AsyncSession = Depends(database.get_db)):
    return await crud.update_party_participant(db=db, participant_id=id, participant=participant)

## 파티방 명단 삭제
@app.delete("/participant/{id}", response_model=schemas.Participant, summary="파티 삭제", tags=["party"])
async def delete_party_participant(id: int, db: AsyncSession = Depends(database.get_db)):
    return await crud.delete_party_participant(db=db, participant_id=id)



# 조 관리
## 조 자동생성

## 조 리스트

## 개별 조 상세정보

## 조 별 매니저 권한 생성


## 조 별 매니저 권한 수정

## 조 별 매니저 권한 삭제







# 매니저 관리
## 매니저 리스트

## 매니저 상세정보

## 매니저 생성

## 매니저 수정

## 매니저 삭제





#  프로그램 관리
## 실시간 참석 on/off

## 실시간 참석 추가 요청

## 강제 퇴장

## 짝 매칭 프로그램 실행


## 파티방 개설
