from fastapi import Depends, HTTPException, Query, APIRouter, status
from ..db import adminService, database, errorLog
from ..utils import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from ..oauth import oauth

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

## admin (관리자 사용 API)
@router.post(
    "/login", 
    response_model=schemas.loginResponse, 
    summary="관리자용 로그인 API")
async def login_admin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(database.get_db)
):
    try:
        user, pw = await adminService.authenticate_admin(db, form_data.username, form_data.password)

        if not user or not pw:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = await oauth.create_access_token(data={
            "sub": str(user.id),
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
    "/accomodations", 
    response_model=schemas.AdminAccomodation, 
    summary="관리자용 게스트 하우스 관리 페이지 - 게스트 하우스 리스트 정보 가져오기 API")
async def read_adminAccomodations(
    isMostReviews: bool = Query(True), 
    name: str = Query(None),
    page: int = Query(0),
    pageSize: int = Query(10), 
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.admin_verify_token)
):
    try:
        if token != "SUPER_ADMIN":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
            
        data = await adminService.get_adminAccomodations(db, isMostReviews, page, pageSize, name)
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
    name: str = Query(None),
    page: int = Query(0),
    pageSize: int = Query(10), 
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.admin_verify_token)
):
    try:
        if token != "SUPER_ADMIN":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        data = await adminService.get_adminOwners(db, isOldestOrders, page, pageSize, name)
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
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.admin_verify_token)
):
    try:
        if token != "SUPER_ADMIN":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
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
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.admin_verify_token)
):
    try:
        if token != "SUPER_ADMIN":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        return await adminService.put_deny_adminOwners(db, id)
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})