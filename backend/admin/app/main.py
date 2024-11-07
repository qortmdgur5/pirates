import os
from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
import urllib.parse
from .db import crud, database
from .utils import schemas
from .oauth import oauth
import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)





@app.post("/admin/password", summary="Admin 로그인 후 토큰 발급", tags=["login"])
async def login_adminpassword(
    username: str, 
    db: AsyncSession = Depends(database.get_db)
):
    password = await crud.get_admin_by_password(db, username)

    return {"password": password}

# Admin 로그인 API
@app.post("/admin/token", summary="Admin 로그인 후 토큰 발급", tags=["login"])
async def login_admin(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = await crud.authenticate_admin(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = oauth.create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

# Manager 로그인 API
@app.post("/manager/token", summary="Manager 로그인 후 토큰 발급", tags=["login"])
async def login_manager(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = await crud.authenticate_manager(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = oauth.create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


## admin (관리자 사용 API)
@app.get("/admin/accomodations", response_model=schemas.AdminAccomodation, summary="관리자용 게스트 하우스 관리 페이지 - 게스트 하우스 리스트 정보 가져오기 API", tags=["admin"])
async def read_adminAccomodations(
    isMostReviews: bool = Query(True), 
    page: int = Query(0),
    pageSize: int = Query(10), 
    db: AsyncSession = Depends(database.get_db),
    # token: str = Depends(oauth.verify_token)
):
    try:
        data = await crud.get_adminAccomodations(db, isMostReviews, page, pageSize)
        return data
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message) 
        raise HTTPException(status_code=500, detail={"msg": "fail"})

@app.get("/admin/owners", response_model=schemas.AdminOwner, summary="관리자용 게스트 하우스 승인 관리 페이지 - 사장님 리스트 정보 가져오기 API", tags=["admin"])
async def read_adminOwners(
    isOldestOrders: bool = Query(True),
    page: int = Query(0),
    pageSize: int = Query(10), 
    db: AsyncSession = Depends(database.get_db)
):
    try:
        data = await crud.get_adminOwners(db, isOldestOrders, page, pageSize)
        return data
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message) 
        raise HTTPException(status_code=500, detail={"msg": "fail"})

@app.put("/admin/owner/auth/{id}", summary="관리자용 게스트 하우스 승인 관리 페이지 - 사장님 승인 API , 승인 요청 시 해당 사장님 role 컬럼을 ROLE_AUTH_OWNER 로 변경", tags=["admin"])
async def update_auth_adminOwners(
    id: int, 
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await crud.put_auth_adminOwners(db, id)
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message) 
        raise HTTPException(status_code=500, detail={"msg": "fail"})

@app.put("/admin/owner/deny/{id}", summary="관리자용 게스트 하우스 승인 관리 페이지 - 사장님 취소 API, 요청 시 사장님 role 컬럼을 ROLE_NOTAUTH_OWNER 로 변경", tags=["admin"])
async def update_deny_adminOwners(
    id: int, 
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await crud.put_deny_adminOwners(db, id)
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})


## owner (사장님 사용 API)
@app.post("/owner/signup", summary="사장님용 회원가입 API, role 데이터는 기본값 미승인 값인 ROLE_NOTAUTH_OWNER로 넣어주셈", tags=["owner"])
async def post_signup_owner(
    data: schemas.signupOwner,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        await crud.create_signup_owner(db, data)
        return {"msg": "ok"}
    except Exception as e:
            error_message = str(e)
            await crud.log_error(db, error_message) 
            raise HTTPException(status_code=500, detail={"msg": "fail"})

      
@app.post("/owner/duplicate", summary="사장님용 아아디 중복검사 API, username 과 동일한 데이터가 있으면 true, 없으면 false", tags=["owner"])
async def post_duplicate_owner(
    username: str,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        data = await crud.create_duplicate_owner(db, username)
        return data
    except Exception as e:
            error_message = str(e)
            await crud.log_error(db, error_message) 
            raise HTTPException(status_code=500, detail={"msg": "fail"})

  
@app.post("/owner/login", response_model=schemas.loginResponse, summary="Owner 로그인 후 토큰 발급", tags=["owner"])
async def login_owner(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(database.get_db)
):
    try:
        user, pw, accomodation_id = await crud.authenticate_owner(db, form_data.username, form_data.password)

        if not user or not pw:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = oauth.create_access_token(data={
            "sub": str(user.id),
            "accomodation_id": accomodation_id,
            "role": user.role
        })
        
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message) 
        raise HTTPException(status_code=500, detail={"msg": "fail"})
       
@app.get("/owner/accomodation/{id}", response_model=schemas.OwnerAccomodationsWithoutDate, summary="사장님용 게스트 하우스 등록 관리 페이지 - 게스트 하우스 정보 가져오기 API", tags=["owner"])
async def read_ownerAccomodation(
    id: int, 
    page: int = Query(0),
    pageSize: int = Query(10), 
    db: AsyncSession = Depends(database.get_db)
):
    try:
        data = await crud.get_ownerAccomodation(id, db, page, pageSize)
        return data
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})


@app.post("/owner/accomodation", summary="사장님용 게스트 하우스 등록 관리 페이지 - 숙소 등록 API, QR 주소 컬럼 추가", tags=["owner"])
async def create_ownerAccomdation(
    accomodation: schemas.OwnerAccomodationsPost,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await crud.post_ownerAccomodation(db, accomodation)
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})


@app.put("/owner/accomodation/{id}", summary="사장님용 게스트 하우스 등록 관리 페이지 - 숙소 수정 API", tags=["owner"])
async def update_ownerAccomodation(
    id: int,
    accomodation: schemas.OwnerAccomodationsPut,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await crud.put_ownerAccomodation(db, id, accomodation)
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})



@app.get("/owner/managers/{id}", response_model=schemas.OwnerManager, summary="사장님용 게스트 하우스 등록 관리 페이지 - 게스트 하우스 정보 가져오기 API", tags=["owner"])
async def read_ownermanagers(
    id: int, 
    isOldestOrders: bool = Query(True), 
    page: int = Query(0),
    pageSize: int = Query(10), 
    db: AsyncSession = Depends(database.get_db)
):
    try:
        data = await crud.get_ownermanagers(id, db, isOldestOrders, page, pageSize)
        return data
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})
    

@app.put("/owner/manager/auth/{id}", summary="사장님용 매니저 등록 관리 페이지 - 매니저 승인 API , 승인 요청 시 해당 매니저 role 컬럼을 ROLE_AUTH_MANAGER 로 변경", tags=["owner"])
async def update_auth_ownerOwners(
    id: int, 
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await crud.put_auth_ownerOwners(db, id)
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})


@app.put("/owner/manager/deny/{id}", summary="사장님용 매니저 등록 관리 페이지 - 매니저 삭제 API , 삭제 요청 시 해당 매니저 정보 삭제", tags=["owner"])
async def update_deny_ownerOwners(
    id: int, 
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await crud.put_deny_ownerOwners(db, id)
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})




## owner , manager(사장님 And 매니저 사용 API)
@app.get("/manager/getAccomodation", summary="매니저용 회원가입 페이지 API, 모든 숙소 리스트 가져오기", tags=["owner , manager"])
async def read_managerGetAccomodation(
    page: int = Query(0),
    pageSize: int = Query(10), 
    db: AsyncSession = Depends(database.get_db)
):
    try:
        data = await crud.get_managerGetAccomodation(db, page, pageSize)
        return data
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message) 
        raise HTTPException(status_code=500, detail={"msg": "fail"})
    
    
@app.post("/mananger/signup", summary="매니저용 회원가입 API, role 데이터는 기본값 미승인 값인 ROLE_NOTAUTH_MANAGER로 넣어주셈", tags=["owner , manager"])
async def post_signup_mananger(
    data: schemas.signupManager,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        await crud.create_signup_mananger(db, data)
        return {"msg": "ok"}
    except Exception as e:
            error_message = str(e)
            await crud.log_error(db, error_message) 
            raise HTTPException(status_code=500, detail={"msg": "fail"})

      
@app.post("/mananger/duplicate", summary="매니저용 아이디 중복검사 API, username 과 동일한 데이터가 있으면 true, 없으면 false", tags=["owner , manager"])
async def post_duplicate_mananger(
    username: str,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        data = await crud.create_duplicate_mananger(db, username)
        return data
    except Exception as e:
            error_message = str(e)
            await crud.log_error(db, error_message) 
            raise HTTPException(status_code=500, detail={"msg": "fail"})

  
@app.post("/mananger/login", response_model=schemas.loginResponse, summary="매니저용 로그인 API", tags=["owner , manager"])
async def login_mananger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(database.get_db)
):
    try:
        user, pw, accomodation_id = await crud.authenticate_mananger(db, form_data.username, form_data.password)

        if not user or not pw:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = oauth.create_access_token(data={
            "sub": str(user.id),
            "accomodation_id": accomodation_id,
            "role": user.role
        })
        
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message) 
        raise HTTPException(status_code=500, detail={"msg": "fail"})
    
    
@app.get("/manager/parties/{id}", response_model=schemas.managerParty, summary="매니저용 파티방 관리 페이지 - 파티방 리스트 가져오기 API", tags=["owner , manager"])
async def read_managerParties(
    id: int, 
    isOldestOrders: bool = Query(True),
    page: int = Query(0),
    pageSize: int = Query(10), 
    db: AsyncSession = Depends(database.get_db)
):
    try:
        data = await crud.get_managerParties(id, db, isOldestOrders, page, pageSize)
        return data
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message) 
        raise HTTPException(status_code=500, detail={"msg": "fail"})


@app.post("/manager/party", summary="매니저용 파티방 관리 페이지 - 파티방 개설 API", tags=["owner , manager"])
async def create_managerParty(
    party: schemas.managerPartiesPost,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await crud.post_managerParty(db, party)
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})
    
    
@app.put("/manager/party/{id}", summary="매니저용 파티방 관리 페이지 - 파티방 수정 API", tags=["owner , manager"])
async def update_managerParty(
    id: int,
    party: schemas.managerPartyUpdate,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await crud.put_managerParty(db, id, party)
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})
    
@app.delete("/manager/party/{id}", summary="매니저용 파티방 관리 페이지 - 파티방 삭제 API, 요청시 해당 파티방 삭제", tags=["owner , manager"])
async def delete_managerParty(
    id: int,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await crud.del_managerParty(db, id)
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})
    
    
    
    
@app.get("/manager/party/{id}", response_model=schemas.managerParticipants, summary="매니저용 파티 상세 페이지 - 파티 상세 정보 가져오기 API", tags=["owner , manager"])
async def read_managerParty(
    id: int, 
    page: int = Query(0),
    pageSize: int = Query(10), 
    db: AsyncSession = Depends(database.get_db)
):
    try:
        data = await crud.get_managerParty(id, db, page, pageSize)
        return data
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})


@app.post("/manager/participant", response_model=schemas.SimpleResponse, summary="매니저용 파티 상세 페이지 - 참석자 추가 API", tags=["owner , manager"])
async def create_managerParticipant(
    party: schemas.managerParticipantPost,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await crud.post_managerParticipant(db, party)
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})
    
    
@app.delete("/manager/participant/{id}", summary="매니저용 파티 상세 페이지 - 참석자 삭제 API, 요청시 해당 참석자 삭제", tags=["owner , manager"])
async def delete_managerParticipant(
    id: int,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await crud.del_managerParticipant(db, id)
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})
    
    
@app.put("/manager/partyOn/{id}", summary="매니저용 파티 상세 페이지 - 파티 ON/OFF API, 요청시 요청값에 따른 파티방 ON/OFF 처리", tags=["owner , manager"])
async def update_managerPartyOn(
    id: int,
    party: schemas.managerPartyOn,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await crud.put_managerPartyOn(db, id, party)
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})
    
@app.get("/manager/accomodation/qr/{id}", summary="QR 코드 주소 데이터 요청", tags=["owner , manager"])
async def read_managerAccomodationQR(
    id: int, 
    db: AsyncSession = Depends(database.get_db)
):
    try:
        file_path  = await crud.get_managerAccomodationQR(id, db)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail={"msg": "QR code file not found"})

        filename = os.path.basename(file_path)
        encoded_filename = urllib.parse.quote(filename)
        
        headers = {
            "Content-Disposition": f"attachment; filename=\"{encoded_filename}\"",
            "Cache-Control": "no-store"
        }
        
        return FileResponse(
            path=file_path, 
            media_type='image/png',
            headers=headers
        )
    except HTTPException as http_exc:
        raise http_exc 
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})