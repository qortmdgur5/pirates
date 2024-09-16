from typing import List
from fastapi import FastAPI, Depends, HTTPException, Request, Path, Body
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
@app.get("/party", response_model=List[schemas.Party] ,summary="날짜별 파티방 리스트", tags=["party"])
async def read_party_list(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
    party = await crud.party_list(db, skip=skip, limit=limit)
    return party

## 전체 명단 리스트
@app.get("/participant/{partyId}", response_model=List[schemas.Participant], summary="날짜별 파티방 명단", tags=["party"])
async def read_party_participant(partyId: int, skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
    participant = await crud.party_participant(db, party_id=partyId, skip=skip, limit=limit)
    return participant


## 파티방 명단 생성
@app.post("/participant", response_model=schemas.Participant, summary="파티방 명단 등록", tags=["party"])
async def create_party_participant(participant: schemas.ParticipantBase, db: AsyncSession = Depends(database.get_db)):
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
async def update_party_participant(id: int, participant: schemas.ParticipantBase, db: AsyncSession = Depends(database.get_db)):
    return await crud.update_party_participant(db=db, participant_id=id, participant=participant)

## 파티방 명단 삭제
@app.delete("/participant/{id}", response_model=schemas.Participant, summary="파티 삭제", tags=["party"])
async def delete_party_participant(id: int, db: AsyncSession = Depends(database.get_db)):
    return await crud.delete_party_participant(db=db, participant_id=id)



# # 조 관리
# ## 조 자동생성
# @app.post("/team", response_model=schemas.PartyTeam, summary="조 자동 생성", tags=["team"])
# async def create_party_team(team: schemas.PartyTeam, db: AsyncSession = Depends(database.get_db)):
#     """
#     파티방 명단 등록.
    
#     - **id**: 파티 아이디.
#     - **totalNumber**: 총 예약 인원 수.
#     - **teamNumber**: 총 파티 조 수.
#     """
#     return await crud.create_team_participant(db=db, team=team)


# ## 조 리스트
# @app.get("/team", response_model=List[schemas.PartyTeam], summary="조 리스트", tags=["team"])
# async def read_party_team(partyId: int, skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
#     party_team_list = await crud.party_team(db, party_id=partyId, skip=skip, limit=limit)
#     return party_team_list


# ## 개별 조 상세정보
# @app.get("/team/{id}", response_model=schemas.PartyTeam, summary="개별 조 상세정보", tags=["team"])
# async def read_party_team(id: int, db: AsyncSession = Depends(database.get_db)):
#     party_team = await crud.get_party_team(db, team_id=id)
#     if party_team is None:
#         raise HTTPException(status_code=404, detail="team not found")
#     return party_team


# ## 조 별 매니저 권한 생성
# @app.post("/team/auth", response_model=schemas.Manager, summary="조 별 매니저 권한 생성", tags=["team"])
# async def create_party_team_auth(manager: schemas.ManagerBase, db: AsyncSession = Depends(database.get_db)):
#     """
#     파티방 명단 등록.
    
#     - **party_id**: 파티 아이디.
#     - **name**: 이름.
#     - **phone**: 핸드폰.
#     - **mbti**: mbti.
#     - **age**: 나이.
#     - **region**: 지역.
#     - **gender**: 성별.
#     """
#     return await crud.create_party_team_auth(db=db, manager=manager)



# ## 조 별 매니저 권한 수정
# @app.put("/pteam/auth/{id}", response_model=schemas.Manager, summary="조 별 매니저 권한 수정", tags=["team"])
# async def update_party_participant(id: int, manager: schemas.ManagerBase, db: AsyncSession = Depends(database.get_db)):
#     return await crud.update_party_team_auth(db=db, team_id=id, manager=manager)


# ## 조 별 매니저 권한 삭제
# @app.delete("/team/auth/{id}", response_model=schemas.Manager, summary="조 별 매니저 권한 삭제", tags=["team"])
# async def delete_party_team_auth(id: int, db: AsyncSession = Depends(database.get_db)):
#     return await crud.delete_party_team_auth(db=db, team_id=id)






# 매니저 관리
## 매니저 리스트
@app.get("/managers", response_model=list[schemas.Manager], summary="매니저 리스트", tags=["manager"])
async def read_managers(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
    managers = await crud.get_managers(db, skip=skip, limit=limit)
    return managers


## 매니저 상세정보
@app.get("/manager/{id}", response_model=schemas.Manager, summary="매니저 조회", tags=["manager"])
async def read_manager(id: int, db: AsyncSession = Depends(database.get_db)):
    manager = await crud.get_manager(db, manager_id=id)
    if manager is None:
        raise HTTPException(status_code=404, detail="Manager not found")
    return manager


## 매니저 생성
@app.post("/manager", response_model=schemas.ManagerCreate, summary="매니저 등록", tags=["manager"])
async def create_manager(manager: schemas.ManagerCreate, db: AsyncSession = Depends(database.get_db)):
    """
    업체 등록.

    - **owner_id**: 사장 테이블 pk.
    - **username**: 매니저 아이디.
    - **password**: 매니저 비밀번호.
    - **role**: 매니저 권한(승인-ROLE_AUTH_MANAGER, 미승인-ROLE_NOTAUTH_MANAGER).
    """
    return await crud.create_manager(db=db, manager=manager)


## 매니저 수정
@app.put("/manager/{id}", response_model=schemas.ManagerCreate, summary="매니저 수정", tags=["manager"])
async def update_manager(id: int, manager: schemas.ManagerCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.update_manager(db=db, manager_id=id, manager=manager)


## 매니저 삭제
@app.delete("/manager/{id}", response_model=schemas.Manager, summary="매니저 삭제", tags=["manager"])
async def delete_manager(id: int, db: AsyncSession = Depends(database.get_db)):
    return await crud.delete_manager(db=db, manager_id=id)




#  프로그램 관리
## 실시간 참석 on/off

## 실시간 참석 추가 요청

## 강제 퇴장

## 짝 매칭 프로그램 실행


## 파티방 개설
