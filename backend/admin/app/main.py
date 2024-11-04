import os
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
import urllib.parse
from .db import crud, database
from .utils import schemas
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

## admim (관리자 사용 API)
@app.get("/admin/accomodations", response_model=list[schemas.AdminAccomodations], summary="관리자용 게스트 하우스 관리 페이지 - 게스트 하우스 리스트 정보 가져오기 API", tags=["admin"])
async def read_adminAccomodations(
    isMostReviews: bool = Query(True), 
    skip: int = Query(0),
    limit: int = Query(10), 
    db: AsyncSession = Depends(database.get_db)):
    try:
        data = await crud.get_adminAccomodations(db, isMostReviews=isMostReviews, skip=skip, limit=limit)
        return data
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message) 
        raise HTTPException(status_code=500, detail={"msg": "fail"})

@app.get("/admin/owners", response_model=list[schemas.AdminOwners], summary="관리자용 게스트 하우스 승인 관리 페이지 - 사장님 리스트 정보 가져오기 API", tags=["admin"])
async def read_adminOwners(
            isOldestOrders: bool = Query(True),
            skip: int = Query(0),
            limit: int = Query(10), 
            db: AsyncSession = Depends(database.get_db)):
    try:
        data = await crud.get_adminOwners(db, isOldestOrders=isOldestOrders, skip=skip, limit=limit)
        return data
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message) 
        raise HTTPException(status_code=500, detail={"msg": "fail"})

@app.put("/admin/owner/auth/{id}", summary="관리자용 게스트 하우스 승인 관리 페이지 - 사장님 승인 API , 승인 요청 시 해당 사장님 role 컬럼을 ROLE_AUTH_OWNER 로 변경", tags=["admin"])
async def update_auth_adminOwners(id: int, db: AsyncSession = Depends(database.get_db)):
    try:
        return await crud.put_auth_adminOwners(db=db, id=id)
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message) 
        raise HTTPException(status_code=500, detail={"msg": "fail"})

@app.put("/admin/owner/deny/{id}", summary="관리자용 게스트 하우스 승인 관리 페이지 - 사장님 취소 API, 요청 시 사장님 role 컬럼을 ROLE_NOTAUTH_OWNER 로 변경", tags=["admin"])
async def update_deny_adminOwners(id: int, db: AsyncSession = Depends(database.get_db)):
    try:
        return await crud.put_deny_adminOwners(db=db, id=id)
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})


## owner (사장님 사용 API)
@app.get("/owner/accomodation/{id}", response_model=list[schemas.OwnerAccomodationsWithoutDates], summary="사장님용 게스트 하우스 등록 관리 페이지 - 게스트 하우스 정보 가져오기 API", tags=["owner"])
async def read_ownerAccomodation(
    id: int, 
    skip: int = Query(0),
    limit: int = Query(10), 
    db: AsyncSession = Depends(database.get_db)):
    try:
        data = await crud.get_ownerAccomodation(id=id, db=db, skip=skip, limit=limit)
        return data
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})


@app.post("/owner/accomodation", summary="사장님용 게스트 하우스 등록 관리 페이지 - 숙소 등록 API, QR 주소 컬럼 추가", tags=["owner"])
async def create_ownerAccomdation(
    accomodation: schemas.OwnerAccomodationsPost,
    db: AsyncSession = Depends(database.get_db)):
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
    db: AsyncSession = Depends(database.get_db)):
    try:
        return await crud.put_ownerAccomodation(db, id, accomodation)
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})



@app.get("/owner/managers/{id}", response_model=list[schemas.OwnerManagers], summary="사장님용 게스트 하우스 등록 관리 페이지 - 게스트 하우스 정보 가져오기 API", tags=["owner"])
async def read_ownermanagers(
    id: int, 
    isOldestOrders: bool = Query(True), 
    skip: int = Query(0),
    limit: int = Query(10), 
    db: AsyncSession = Depends(database.get_db)):
    try:
        data = await crud.get_ownermanagers(id, db, isOldestOrders, skip, limit)
        return data
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})
    

@app.put("/owner/manager/auth/{id}", summary="사장님용 매니저 등록 관리 페이지 - 매니저 승인 API , 승인 요청 시 해당 매니저 role 컬럼을 ROLE_AUTH_MANAGER 로 변경", tags=["owner"])
async def update_auth_ownerOwners(id: int, db: AsyncSession = Depends(database.get_db)):
    try:
        return await crud.put_auth_ownerOwners(db, id)
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})


@app.put("/owner/manager/deny/{id}", summary="사장님용 매니저 등록 관리 페이지 - 매니저 삭제 API , 삭제 요청 시 해당 매니저 정보 삭제", tags=["owner"])
async def update_deny_ownerOwners(id: int, db: AsyncSession = Depends(database.get_db)):
    try:
        return await crud.put_deny_ownerOwners(db, id)
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})




## owner , manager(사장님 And 매니저 사용 API)
@app.get("/manager/parties/{id}", response_model=list[schemas.managerParties], summary="매니저용 파티방 관리 페이지 - 파티방 리스트 가져오기 API", tags=["owner , manager"])
async def read_managerParties(
    id: int, 
    isOldestOrders: bool = Query(True),
    skip: int = Query(0),
    limit: int = Query(10), 
    db: AsyncSession = Depends(database.get_db)):
    try:
        data = await crud.get_managerParties(id, db, isOldestOrders, skip, limit)
        return data
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message) 
        raise HTTPException(status_code=500, detail={"msg": "fail"})


@app.post("/manager/party", summary="매니저용 파티방 관리 페이지 - 파티방 개설 API", tags=["owner , manager"])
async def create_managerParty(
    party: schemas.managerParties,
    db: AsyncSession = Depends(database.get_db)):
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
    db: AsyncSession = Depends(database.get_db)):
    try:
        return await crud.put_managerParty(db, id, party)
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})
    
@app.delete("/manager/party/{id}", summary="매니저용 파티방 관리 페이지 - 파티방 삭제 API, 요청시 해당 파티방 삭제", tags=["owner , manager"])
async def delete_managerParty(
    id: int,
    db: AsyncSession = Depends(database.get_db)):
    try:
        return await crud.del_managerParty(db, id)
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})
    
    
    
    
@app.get("/manager/party/{id}", response_model=list[schemas.managerParticipant], summary="매니저용 파티 상세 페이지 - 파티 상세 정보 가져오기 API", tags=["owner , manager"])
async def read_managerParty(
    id: int, 
    skip: int = Query(0),
    limit: int = Query(10), 
    db: AsyncSession = Depends(database.get_db)):
    try:
        data = await crud.get_managerParty(id=id, db=db, skip=skip, limit=limit)
        return data
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})


@app.post("/manager/participant", response_model=schemas.SimpleResponse, summary="매니저용 파티 상세 페이지 - 참석자 추가 API", tags=["owner , manager"])
async def create_managerParticipant(
    party: schemas.managerParticipantPost,
    db: AsyncSession = Depends(database.get_db)):
    try:
        return await crud.post_managerParticipant(db, party)
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})
    
    
@app.delete("/manager/participant/{id}", summary="매니저용 파티 상세 페이지 - 참석자 삭제 API, 요청시 해당 참석자 삭제", tags=["owner , manager"])
async def delete_managerParticipant(
    id: int,
    db: AsyncSession = Depends(database.get_db)):
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
    db: AsyncSession = Depends(database.get_db)):
    try:
        return await crud.put_managerPartyOn(db, id, party)
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": "fail"})
    
@app.get("/manager/accomodation/qr/{id}", summary="QR 코드 주소 데이터 요청", tags=["owner , manager"])
async def read_managerAccomodationQR(
    id: int, 
    db: AsyncSession = Depends(database.get_db)):
    try:
        file_path  = await crud.get_managerAccomodationQR(id=id, db=db)
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