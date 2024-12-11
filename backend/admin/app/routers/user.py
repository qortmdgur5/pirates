from fastapi import APIRouter
from fastapi import Depends, HTTPException, Query, APIRouter
from ..db import errorLog, userService, database
from ..utils import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from ..oauth import kakaoLogin
from fastapi.responses import RedirectResponse

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

## user
@router.get( 
    "/auth/kakao/login/{id}", 
    summary="카카오 로그인 API")
async def kakao_login(
    id: int,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        kakao_auth_url = await kakaoLogin.kakao_login_data(id, db)
        return RedirectResponse(kakao_auth_url)
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
    
    
@router.get(
    "/auth/kakao/callback", 
    summary="카카오 로그인 콜백 API")
async def kakao_callback(
    code: str, 
    state: str,
    db: AsyncSession = Depends(database.get_db)
    ):
    """
    code: 카카오가 리디렉션 URL로 전달하는 Authorization Code
    """
    try:
        id = int(state) 
        user_info = await kakaoLogin.kakao_callback_data(db, code, id)
        return await userService.post_userLoginKakaoCallback(db, user_info["user_info"], user_info["id"])
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
            

@router.post(
    "/signup", 
    summary="유저 회원가입 API - 최초 로그인인 경우 - 로그인 API 를 탔을때 userInfo 데이터가 Null 일 경우 회원가입 페이지로 이동하여 추가정보를 저장할 API")
async def create_userSignup(
    userSignup: schemas.userSignupResponse,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        return await userService.post_userSignup(db, userSignup)
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})

@router.get(
    "/party/{id}", 
    response_model=schemas.userPartyResponse, 
    summary="게스트 하우스의 당일 파티정보 가져오기 API")
async def read_userPartyInto( 
    id: int,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        userParty = schemas.userPartyRequest(party_id=id)
        data = await userService.get_userParty(db, userParty)
        return data
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})


@router.get(
    "/partyInfo/{party_id}", 
    response_model=schemas.userPartyIntoResponse, 
    summary="User 테이블의 party_id 에 해당하는 유저들의 정보를 가져오는 API - PartyUserInfo 테이블의 해당 유저의 partyOn 데이터가 true 인 경우의 유저들 정보만 가져오기")
async def read_userPartyInto( 
    party_id: int, 
    page: int = Query(0),
    pageSize: int = Query(10), 
    db: AsyncSession = Depends(database.get_db)
):
    try:
        data = await userService.get_userPartyInto(party_id, db, page, pageSize)
        return data
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
