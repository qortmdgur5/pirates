from fastapi import APIRouter
from fastapi import Depends, HTTPException, Query, APIRouter
from ..db import adminService, database, errorLog
from ..utils import schemas
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

## admin (관리자 사용 API)
@router.get(
    "/accomodations", 
    response_model=schemas.AdminAccomodation, 
    summary="관리자용 게스트 하우스 관리 페이지 - 게스트 하우스 리스트 정보 가져오기 API")
async def read_adminAccomodations(
    isMostReviews: bool = Query(True), 
    page: int = Query(0),
    pageSize: int = Query(10), 
    db: AsyncSession = Depends(database.get_db),
    # token: str = Depends(oauth.verify_token)
):
    try:
        data = await adminService.get_adminAccomodations(db, isMostReviews, page, pageSize)
        return data
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})

@router.get(
    "/owners", 
    response_model=schemas.AdminOwner, 
    summary="관리자용 게스트 하우스 승인 관리 페이지 - 사장님 리스트 정보 가져오기 API")
async def read_adminOwners(
    isOldestOrders: bool = Query(True),
    page: int = Query(0),
    pageSize: int = Query(10), 
    db: AsyncSession = Depends(database.get_db)
):
    try:
        data = await adminService.get_adminOwners(db, isOldestOrders, page, pageSize)
        return data
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})

@router.put(
    "/owner/auth/{id}", 
    summary="관리자용 게스트 하우스 승인 관리 페이지 - 사장님 승인 API , 승인 요청 시 해당 사장님 role 컬럼을 ROLE_AUTH_OWNER 로 변경")
async def update_auth_adminOwners(
    id: int, 
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await adminService.put_auth_adminOwners(db, id)
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})

@router.put(
    "/owner/deny/{id}", 
    summary="관리자용 게스트 하우스 승인 관리 페이지 - 사장님 취소 API, 요청 시 사장님 role 컬럼을 ROLE_NOTAUTH_OWNER 로 변경")
async def update_deny_adminOwners(
    id: int, 
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await adminService.put_deny_adminOwners(db, id)
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})