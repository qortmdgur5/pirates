import json
import os
from fastapi import Depends, HTTPException, APIRouter, Query, WebSocket, WebSocketDisconnect, status
from ..db import errorLog, userService, database
from ..utils import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from ..oauth import kakaoLogin, oauth
from fastapi.responses import RedirectResponse
from typing import Optional, List

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

## user
@router.get( 
    "/auth/kakao/login", 
    summary="카카오 로그인 API")
async def kakao_login(
    id: Optional[str] = None,
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
    state: Optional[str] = None,
    db: AsyncSession = Depends(database.get_db)
    ):
    """
    code: 카카오가 리디렉션 URL로 전달하는 Authorization Code
    """
    try:
        user_info = await kakaoLogin.kakao_callback_data(db, code, state)
        grouped_data = await userService.post_userLoginKakaoCallback(db, user_info["user_info"], user_info["id"])
        access_token = await oauth.create_access_token(data={"data": grouped_data})

        ip_address = os.getenv("BACKEND_IP")
        port = os.getenv("FRONTEND_PORT")
        redirect_url = f"http://{ip_address}:{port}/user/login/success?access_token={access_token}"
        
        return RedirectResponse(url=redirect_url)
    
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
async def read_userPartyInfo( 
    id: int,
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.user_verify_token)
):
    try:
        if token != "ROLE_USER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
            
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
    "/party/matchTime/{party_id}", 
    summary="Party 테이블 짝매칭 시작시간(matchStartTime 필드) 가져오기 API")
async def read_userPartyInfo( 
    party_id: int,
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.user_verify_token)
):
    try:
        if token != "ROLE_USER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        data = await userService.get_userPartyMatchTime(db, party_id)
        return data
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
    

@router.get(
    "/partyInfo/{party_id}", 
    response_model=schemas.userPartyInfoResponse, 
    summary="User 테이블의 party_id 에 해당하는 유저들의 정보를 가져오는 API - PartyUserInfo 테이블의 해당 유저의 partyOn 데이터가 true 인 경우의 유저들 정보만 가져오기")
async def read_userPartyInfo( 
    party_id: int, 
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.user_verify_token)
):
    try:
        if token != "ROLE_USER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        data = await userService.get_userPartyInfo(party_id, db)
        return data
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
    
    
@router.get(
    "/partyInfo/chatExist/{party_id}/{user_id}", 
    response_model=schemas.userPartyInfoChatExistResponse, 
    summary="ChatRoom 테이블의 party_id = party_id & ( user_id_1 = user_id OR user_id_2 = user_id ) 조건에 해당하는 데이터")
async def read_userPartyInfoChatExist( 
    party_id: int, 
    user_id: int,
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.user_verify_token)
):
    try:
        if token != "ROLE_USER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        data = await userService.get_userPartyInfoChatExist(party_id, user_id, db)
        return data
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
    
    
    
@router.post(
    "/chatRoom", 
    summary="채팅방 생성 API")
async def create_userChatRoom(
    userChatRoomRequest: schemas.userChatRoomRequest,
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.user_verify_token)
):
    try:
        if token != "ROLE_USER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        return await userService.post_userChatRoom(db, userChatRoomRequest)
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
    

@router.post(
    "/chatRooms", 
    summary="ChatRoom 테이블의 동일한 해당 유저의 채팅방 리스트 가져오기 API")
async def create_userChatRooms(
    userChatRoomsRequest: schemas.userChatRoomsRequest,
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.user_verify_token)
):
    try:
        if token != "ROLE_USER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        return await userService.post_userChatRooms(db, userChatRoomsRequest)
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
    
@router.post(
    "/chat/contents", 
    summary="해당 채팅방의 채팅 내역 가져오기 API")
async def create_userChatContents(
    userChatContentsRequest: schemas.userChatContentsRequest,
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.user_verify_token)
):
    try:
        if token != "ROLE_USER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        return await userService.post_userChatContents(db, userChatContentsRequest)
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
    
@router.post(
    "/chat",
    summary="채팅 전송(생성) API")
async def create_chat(
    chat: schemas.chatCreateRequest, 
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.user_verify_token)
    ):
    try:
        if token != "ROLE_USER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        return await userService.post_chat(db, chat)

    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})


manager = userService.ConnectionManager()

@router.websocket("/ws/chat/{chatRoom_id}/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    chatRoom_id: int, 
    user_id: int,
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.user_verify_token)
):
    
    try:
        if token != "ROLE_USER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        await manager.connect(websocket, chatRoom_id, user_id)
        while True:
            data = await websocket.receive_text()
            chat = schemas.chatCreateRequest(user_id=user_id, contents=data, chatRoom_id=chatRoom_id)
            await userService.post_chat(db, chat)
            
            chat_id = await userService.get_chatId(db, chatRoom_id, user_id)
            message = json.dumps({
                "user_id": user_id,
                "chatRoom_id": chatRoom_id,
                "chat_id": chat_id,
                "content": data,
            }, ensure_ascii=False)

            await manager.broadcast(message, chatRoom_id)
            
    except WebSocketDisconnect:
        await manager.disconnect(chatRoom_id, user_id)
        await manager.broadcast(f"User {user_id} left ChatRoom {chatRoom_id}", chatRoom_id)
        

@router.post(
    "/chat/lastReadChat",
    summary="해당 채팅방의 마지막 읽은 채팅이 무엇인지 알게 해주는 상태 업데이트 API")
async def create_lastReadChat(
    chat: schemas.lastReadChatRequest, 
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.user_verify_token)
    ):
    try:
        if token != "ROLE_USER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        return await userService.post_lastReadChat(db, chat)

    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})

@router.post(
    "/match/userList", 
    response_model=schemas.userMatchUserListResponse, 
    summary="짝매칭 같은 조 유저 리스트 가져오기 API")
async def read_userMatchUserList( 
    userList: schemas.userMatchUserListRequest, 
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.user_verify_token)
):
    try:
        if token != "ROLE_USER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        data = await userService.get_userMatchUserList(userList, db)
        return data
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
    


@router.post(
    "/match/select", 
    summary="짝 매칭 선택 API")
async def create_userMatchSelect(
    userChatRoomRequest: schemas.userChatRoomRequest,
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.user_verify_token)
):
    try:
        if token != "ROLE_USER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        return await userService.post_userMatchSelect(db, userChatRoomRequest)
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
    
    
@router.get(
    "/match/confirm/{party_id}/{user_id}", 
    response_model=schemas.userMatchConfirmResponse, 
    summary="짝 매칭 결과보기 API")
async def read_userMatchConfirm( 
    party_id: int, 
    user_id: int,
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.user_verify_token)
):
    try:
        if token != "ROLE_USER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        data = await userService.get_userMatchConfirm(party_id, user_id, db)
        return data
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
    
    
@router.get(
    "/match/select/{party_id}", 
    response_model=schemas.userMatchSelectResponse, 
    summary="짝 매칭 결과보기 API")
async def read_userMatchSelect( 
    party_id: int, 
    db: AsyncSession = Depends(database.get_db),
    token: str = Depends(oauth.user_verify_token)
):
    try:
        if token != "ROLE_USER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        data = await userService.get_userMatchSelect(party_id, db)
        return data
    except ValueError as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        await errorLog.log_error(db, str(e))
        raise HTTPException(status_code=500, detail={"msg": str(e)})
    