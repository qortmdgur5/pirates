from fastapi import APIRouter
from fastapi import Depends, HTTPException, Query, status, APIRouter
from fastapi.responses import FileResponse
from ..db import errorLog, managerService, database
from ..utils import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from ..oauth import oauth
import os
import urllib.parse

router = APIRouter(
    prefix="/manager",
    tags=["owner , manager"],
)

## owner , manager(사장님 And 매니저 사용 API)
@router.get(
    "/getAccomodation", 
    summary="매니저용 회원가입 페이지 API, 모든 숙소 리스트 가져오기")
async def read_managerGetAccomodation(
    db: AsyncSession = Depends(database.get_db)
):
    try:
        data = await managerService.get_managerGetAccomodation(db)
        return data
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
    
    
@router.post(
    "/signup", 
    summary="매니저용 회원가입 API, role 데이터는 기본값 미승인 값인 ROLE_NOTAUTH_MANAGER로 넣어주셈")
async def post_signup_mananger(
    data: schemas.signupManager,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        await managerService.create_signup_mananger(db, data)
        return {"msg": "ok"}
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})

      
@router.post(
    "/duplicate", 
    summary="매니저용 아이디 중복검사 API, username 과 동일한 데이터가 있으면 true, 없으면 false")
async def post_duplicate_mananger(
    username: str,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        data = await managerService.create_duplicate_mananger(db, username)
        return data
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})

  
@router.post(
    "/login", 
    response_model=schemas.loginResponse, 
    summary="매니저용 로그인 API")
async def login_mananger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(database.get_db)
):
    try:
        user, pw, accomodation_id = await managerService.authenticate_mananger(db, form_data.username, form_data.password)

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
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
    
    
@router.get(
    "/parties/{id}", 
    response_model=schemas.managerParty, 
    summary="매니저용 파티방 관리 페이지 - 파티방 리스트 가져오기 API")
async def read_managerParties(
    id: int, 
    isOldestOrders: bool = Query(True),
    page: int = Query(0),
    pageSize: int = Query(10), 
    db: AsyncSession = Depends(database.get_db)
):
    try:
        data = await managerService.get_managerParties(id, db, isOldestOrders, page, pageSize)
        return data
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})


@router.post(
    "/party", 
    summary="매니저용 파티방 관리 페이지 - 파티방 개설 API")
async def create_managerParty(
    party: schemas.managerPartiesPost,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await managerService.post_managerParty(db, party)
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
    
@router.put(
    "/party/{id}", 
    summary="매니저용 파티방 관리 페이지 - 파티방 수정 API")
async def update_managerParty(
    id: int,
    party: schemas.managerPartyUpdate,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await managerService.put_managerParty(db, id, party)
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
    
@router.delete(
    "/party/{id}", 
    summary="매니저용 파티방 관리 페이지 - 파티방 삭제 API, 요청시 해당 파티방 삭제")
async def delete_managerParty(
    id: int,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await managerService.del_managerParty(db, id)
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
    

@router.get(
    "/party/{id}", 
    response_model=schemas.managerParticipants, 
    summary="매니저용 파티 상세 페이지 - 파티 상세 정보 가져오기 API")
async def read_managerParty(
    id: int, 
    page: int = Query(0),
    pageSize: int = Query(10), 
    db: AsyncSession = Depends(database.get_db)
):
    try:
        data = await managerService.get_managerParty(id, db, page, pageSize)
        return data
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})


@router.post(
    "/participant", 
    response_model=schemas.SimpleResponse, 
    summary="매니저용 파티 상세 페이지 - 참석자 추가 API")
async def create_managerParticipant(
    party: schemas.managerParticipantPost,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await managerService.post_managerParticipant(db, party)
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
    
    
@router.delete(
    "/participant/{id}", 
    summary="매니저용 파티 상세 페이지 - 참석자 삭제 API, 요청시 해당 참석자 삭제")
async def delete_managerParticipant(
    id: int,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await managerService.del_managerParticipant(db, id)
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
    
@router.put(
    "/partyOn/{id}", 
    summary="매니저용 파티 상세 페이지 - 파티 ON/OFF API, 요청시 요청값에 따른 파티방 ON/OFF 처리")
async def update_managerPartyOn(
    id: int,
    party: schemas.managerPartyOn,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await managerService.put_managerPartyOn(db, id, party)
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
    
@router.get(
    "/accomodation/qr/{id}", 
    summary="QR 코드 주소 데이터 요청")
async def read_managerAccomodationQR(
    id: int, 
    db: AsyncSession = Depends(database.get_db)
):
    try:
        file_path  = await managerService.get_managerAccomodationQR(id, db)
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
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})


@router.get(
    "/partyInfo/{id}", 
    summary="User 테이블의 party_id 에 해당하는 유저들의 정보를 가져오는 API - PartyUserInfo 테이블의 해당 유저의 partyOn 데이터가 true, false 모든 유저들 정보 가져오기")
async def read_managerPartyInfo(
    id: int, 
    db: AsyncSession = Depends(database.get_db)
):
    try:
        data = await managerService.get_managerPartyInfo(id, db)
        return data
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})


@router.put(
    "/partyUserInfo", 
    summary="매니저용 파티 유저 리스트 페이지 - 유저의 PartyUserInfo 테이블 team 조 배정 및 수정 API")
async def update_managerPartyUserInfo(
    data: schemas.managerPartyUserInfoDatas,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await managerService.put_managerPartyUserInfo(db, data)
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
    
    
@router.put(
    "/partyUserOn/{id}", 
    summary="매니저용 파티 유저 리스트 페이지 - 유저의 partyOn 상태 변경 API")
async def update_managerPartyUserOn(
    id: int,
    partyOn: bool,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await managerService.put_managerPartyUserOn(id, db, partyOn)
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
    
@router.put(
    "/party/matchStart/{id}", 
    summary="매니저용 파티 유저 리스트 페이지 - 유저의 partyOn 상태 변경 API")
async def update_managerPartyMatchStart(
    id: int,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await managerService.put_managerPartyMatchStart(id, db)
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})