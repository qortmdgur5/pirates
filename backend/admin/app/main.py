from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from .db import crud, database
from .utils import schemas
import logging

app = FastAPI()

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


@app.post("/owner/accomodation", summary="사장님용 게스트 하우스 등록 관리 페이지 - 숙소 등록 API", tags=["owner"])
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
    skip: int = Query(0),
    limit: int = Query(10), 
    db: AsyncSession = Depends(database.get_db)):
    try:
        data = await crud.get_managerParties(id=id, db=db, skip=skip, limit=limit)
        return data
    except Exception as e:
        error_message = str(e)
        await crud.log_error(db, error_message)  # 에러 로그 저장
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