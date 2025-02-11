from fastapi import APIRouter
from fastapi import Depends, HTTPException, Query, status, APIRouter
from ..db import errorLog, ownerService,  database
from ..utils import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from ..oauth import oauth

router = APIRouter(
    prefix="/owner",
    tags=["owner"],
)


## owner (사장님 사용 API)
@router.post(
    "/signup", 
    summary="사장님용 회원가입 API, role 데이터는 기본값 미승인 값인 ROLE_NOTAUTH_OWNER로 넣어주셈")
async def post_signup_owner(
    data: schemas.signupOwner,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        await ownerService.create_signup_owner(db, data)
        return {"msg": "ok"}
    except Exception as e:
            error_message = str(e)
            await errorLog.log_error(db, error_message) 
            raise HTTPException(status_code=500, detail={"msg": error_message})

      
@router.post(
    "/duplicate", 
    summary="사장님용 아아디 중복검사 API, username 과 동일한 데이터가 있으면 true, 없으면 false")
async def post_duplicate_owner(
    username: str,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        data = await ownerService.create_duplicate_owner(db, username)
        return data
    except Exception as e:
            error_message = str(e)
            await errorLog.log_error(db, error_message) 
            raise HTTPException(status_code=500, detail={"msg": error_message})

  
@router.post(
    "/login", 
    response_model=schemas.loginResponse, 
    summary="Owner 로그인 후 토큰 발급")
async def login_owner(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(database.get_db)
):
    try:
        user, pw, accomodation_id = await ownerService.authenticate_owner(db, form_data.username, form_data.password)

        if not user or not pw:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = await oauth.create_access_token(data={
            "sub": str(user.id),
            "accomodation_id": accomodation_id,
            "role": user.role
        })
        
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        error_message = str(e)
        await errorLog.log_error(db, error_message) 
        raise HTTPException(status_code=300, detail={"msg": error_message})
       
@router.get(
    "/accomodation/{id}", 
    response_model=schemas.OwnerAccomodationsWithoutDate, 
    summary="사장님용 게스트 하우스 등록 관리 페이지 - 게스트 하우스 정보 가져오기 API")
async def read_ownerAccomodation(
    id: int, 
    page: int = Query(0),
    pageSize: int = Query(10), 
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.owner_verify_token)
):
    try:
        print(token)
        if token not in ["ROLE_AUTH_OWNER", "ROLE_NOTAUTH_OWNER"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        data = await ownerService.get_ownerAccomodation(id, db, page, pageSize)
        return data
    except Exception as e:
        error_message = str(e)
        await errorLog.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": error_message})


@router.post(
    "/accomodation", 
    summary="사장님용 게스트 하우스 등록 관리 페이지 - 숙소 등록 API, QR 주소 컬럼 추가")
async def create_ownerAccomdation(
    accomodation: schemas.OwnerAccomodationsPost,
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.owner_verify_token)
):
    try:
        if token not in ["ROLE_AUTH_OWNER", "ROLE_NOTAUTH_OWNER"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        return await ownerService.post_ownerAccomodation(db, accomodation)
    except Exception as e:
        error_message = str(e)
        await errorLog.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": error_message})


@router.put(
    "/accomodation/{id}", 
    summary="사장님용 게스트 하우스 등록 관리 페이지 - 숙소 수정 API")
async def update_ownerAccomodation(
    id: int,
    accomodation: schemas.OwnerAccomodationsPut,
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.owner_verify_token)
):
    try:
        if token not in ["ROLE_AUTH_OWNER", "ROLE_NOTAUTH_OWNER"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        return await ownerService.put_ownerAccomodation(db, id, accomodation)
    except Exception as e:
        error_message = str(e)
        await errorLog.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": error_message})



@router.get(
    "/managers/{id}", 
    response_model=schemas.OwnerManager, 
    summary="사장님용 게스트 하우스 등록 관리 페이지 - 게스트 하우스 정보 가져오기 API")
async def read_ownermanagers(
    id: int, 
    isOldestOrders: bool = Query(True), 
    page: int = Query(0),
    pageSize: int = Query(10), 
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.owner_verify_token)
):
    try:
        if token != "ROLE_AUTH_OWNER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        data = await ownerService.get_ownermanagers(id, db, isOldestOrders, page, pageSize)
        return data
    except Exception as e:
        error_message = str(e)
        await errorLog.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": error_message})
    

@router.put(
    "/manager/auth/{id}", 
    summary="사장님용 매니저 등록 관리 페이지 - 매니저 승인 API , 승인 요청 시 해당 매니저 role 컬럼을 ROLE_AUTH_MANAGER 로 변경")
async def update_auth_ownerOwners(
    id: int, 
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.owner_verify_token)
):
    try:
        if token != "ROLE_AUTH_OWNER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        return await ownerService.put_auth_ownerOwners(db, id)
    except Exception as e:
        error_message = str(e)
        await errorLog.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": error_message})


@router.put(
    "/manager/deny/{id}", 
    summary="사장님용 매니저 등록 관리 페이지 - 매니저 삭제 API , 삭제 요청 시 해당 매니저 정보 삭제")
async def update_deny_ownerOwners(
    id: int, 
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.owner_verify_token)
):
    try:
        if token != "ROLE_AUTH_OWNER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        return await ownerService.put_deny_ownerOwners(db, id)
    except Exception as e:
        error_message = str(e)
        await errorLog.log_error(db, error_message)  
        raise HTTPException(status_code=500, detail={"msg": error_message})