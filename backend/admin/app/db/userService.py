from fastapi.websockets import WebSocketState
from sqlalchemy import func, select, and_, or_, case
from sqlalchemy.orm import selectinload, aliased
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, WebSocket, WebSocketDisconnect
from websockets import ConnectionClosed
from .errorLog import format_date, log_error, format_dates
from ..utils import models, schemas
from typing import List, Optional, Dict
from datetime import datetime, timedelta, timezone, time
from itertools import groupby
import asyncio

## user
## 카카오 로그인 
## qr api -> "/user/auth/kakao/login" -> 채팅방 url 이동 api 
def get_kst_now():
    return datetime.now(timezone(timedelta(hours=9)))

async def get_user_info(db: AsyncSession, user_id: str):
    query = select(
        models.User.id,
        models.User.party_id,
        models.UserInfo.user_id,
        models.UserInfo.name,
        models.UserInfo.phone,
        models.UserInfo.gender,
        models.UserInfo.job,
        models.UserInfo.age,
        models.UserInfo.mbti,
        models.UserInfo.region,
    ).join(
        models.UserInfo, models.UserInfo.user_id == models.User.id, isouter=True
    ).where(models.User.id == user_id)

    result = await db.execute(query)
    return result.all()
  
async def get_party_id_for_accommodation(db: AsyncSession, accomodation_id: str, query_date: str):
    query_accomodation = select(models.Party.id).where(
        and_(
            models.Party.accomodation_id == accomodation_id,
            models.Party.partyDate == query_date
        )
    )
    result_party = await db.execute(query_accomodation)
    return result_party.scalar()
  
async def post_userLoginKakaoCallback(
    db: AsyncSession, 
    user_info_dict: dict,
    accomodation_id: Optional[str]
):
    try:
        kst_now = get_kst_now()
        current_time = kst_now.time()
        today_kst = kst_now.date()
        yesterday_kst = today_kst - timedelta(days=1)
        
        if time(hour=0) <= current_time < time(hour=12):  
            query_date = yesterday_kst  # 전날 파티 (단, 정오 이전 데이터만)
        elif time(hour=18) <= current_time:  
            query_date = today_kst  # 당일 파티
        else:
            query_date = None  # 12:00 ~ 17:59는 party_id 제공 X

        username = user_info_dict.get("id")
        nickname = user_info_dict.get("properties", {}).get("nickname")

        existing_user = await db.execute(select(models.User).where(models.User.username == username))
        user = existing_user.scalars().first()
  
        # 큐알 접속이 아니라 url 접근
        if accomodation_id in [None, "", "None"]:
            # 유저 정보가 없을 때
            if not user:
                new_user = models.User(username=username, nickname=nickname, date=kst_now, role="ROLE_USER")
                db.add(new_user)
                await db.commit()
                await db.refresh(new_user)

                grouped_data = [{
                    "id": new_user.id,
                    "role": new_user.role,
                    "party_id": None,
                    "userInfo": []
                }]
                
                return grouped_data
            
            # 유저 정보가 있을 때
            else:
                user_info = await get_user_info(db, user.id)

                grouped_data = []
                rows_sorted = sorted(user_info, key=lambda x: x[0])

                for user_id, group in groupby(rows_sorted, key=lambda x: x[0]):
                    user_info_list = [
                        {
                            "name": info[3],
                            "phone": info[4],
                            "gender": info[5],
                            "job": info[6],
                            "age": info[7],
                            "mbti": info[8],
                            "region": info[9],
                        }
                        for info in group if info[3] is not None
                    ]

                    grouped_data.append({
                        "id": user_id,
                        "role": user.role,
                        "party_id": user.party_id,
                        "userInfo": user_info_list if user_info_list else []
                    })
                return grouped_data
        
        # 큐알 접속 시
        else:
            # 유저 정보가 없을 때
            if not user:
                party_id = await get_party_id_for_accommodation(db, accomodation_id, query_date)

                new_user = models.User(username=username, party_id=party_id, nickname=nickname, date=kst_now, role="ROLE_USER")
                db.add(new_user)
                await db.commit()
                await db.refresh(new_user)

                grouped_data = [{
                    "id": new_user.id,
                    "role": new_user.role,
                    "party_id": party_id,
                    "userInfo": []
                }]
                return grouped_data
            
            # 유저 정보가 있을 때
            else:
                # 파티 아이디가 없을 때
                if not user.party_id:
                    party_id = await get_party_id_for_accommodation(db, accomodation_id, query_date)

                    user.party_id = party_id if party_id else user.party_id
                    user.role = "ROLE_USER"
                    db.add(user)
                    await db.commit()
                    await db.refresh(user)

                # 파티 아이디가 없을 때나 있을 때
                user_info = await get_user_info(db, user.id)

                grouped_data = []
                rows_sorted = sorted(user_info, key=lambda x: x[0])

                for user_id, group in groupby(rows_sorted, key=lambda x: x[0]):
                    user_info_list = [
                        {
                            "name": info[3],
                            "phone": info[4],
                            "gender": info[5],
                            "job": info[6],
                            "age": info[7],
                            "mbti": info[8],
                            "region": info[9],
                        }
                        for info in group if info[3] is not None
                    ]

                    grouped_data.append({
                        "id": user_id,
                        "role": user.role,
                        "party_id": user.party_id,
                        "userInfo": user_info_list if user_info_list else None,
                    })

                return grouped_data

                


    except SQLAlchemyError as e:
        error_message = str(e)
        print("SQLAlchemyError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail="Database Error")
    except ValueError as e:
        error_message = str(e)
        print("ValueError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": error_message})
    except Exception as e:
        error_message = str(e)
        print("Exception:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail={"msg": error_message})


async def post_userSignup(
    db: AsyncSession, 
    userSignup: schemas.userSignupResponse
):
    try:
        user = await db.get(models.User, userSignup.user_id)
        if not user:
            raise HTTPException(status_code=400, detail="User not found")

        db_userInfo = models.UserInfo(
            user_id = userSignup.user_id,
            name = userSignup.name,
            phone = userSignup.phone,
            email = userSignup.email,
            gender = userSignup.gender,
            job = userSignup.job,
            age = userSignup.age,
            mbti = userSignup.mbti,   
            region = userSignup.region
        )
        db.add(db_userInfo)
        await db.commit()
        await db.refresh(db_userInfo)

        return {"msg": "ok"}  
        
    except SQLAlchemyError as e:
        error_message = str(e)
        print("SQLAlchemyError:", error_message) 
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail="Database Error")
    except ValueError as e:
        error_message = str(e)
        print("ValueError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": error_message})
    except Exception as e:
        error_message = str(e)
        print("Exception:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail={"msg": error_message})


async def get_userParty(
    db: AsyncSession,
    userParty: Optional[schemas.userPartyRequest]
) -> List[dict]:
    try:
        query = (
            select(models.Accomodation.name,
                models.Accomodation.introduction,
                models.Accomodation.address,
                models.Accomodation.number,
                models.Owner.phoneNumber,
                models.Accomodation.score,
                models.Accomodation.loveCount,
                models.Party.partyOn,
                models.Party.matchStartTime
            )
            .select_from(models.Party) 
            .join(models.Accomodation, models.Party.accomodation_id == models.Accomodation.id)
            .join(models.Owner, models.Accomodation.owner_id == models.Owner.id) 
            .filter(models.Party.id == userParty.party_id)
        )

        result = await db.execute(query)
        party = result.first()

        response = [
                {
                    "name": party.name, 
                    "introduction": party.introduction,
                    "address": party.address,
                    "number": party.number,
                    "phoneNumber": party.phoneNumber,
                    "score": party.score,
                    "loveCount": party.loveCount,
                    "party_id": userParty.party_id,
                    "party_on": party.partyOn,
                    "matchStartTime": format_dates(party.matchStartTime) if party.matchStartTime else None
                }
            ]
        return {
            "data": response,
            "totalCount": 0
        } 
    
    except SQLAlchemyError as e:
        error_message = str(e)
        print("SQLAlchemyError:", error_message) 
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail="Database Error")
    except ValueError as e:
        error_message = str(e)
        print("ValueError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": error_message})
    except Exception as e:
        error_message = str(e)
        print("Exception:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail={"msg": error_message})


async def get_userPartyMatchTime(
    db: AsyncSession,
    party_id: int
) -> List[dict]:
    try:
        query = (
            select(models.Party.matchStartTime)
            .where(models.Party.id == party_id)
        )

        result = await db.execute(query)
        party = result.first()

        response = {"matchStartTime": format_dates(party.matchStartTime) if party.matchStartTime else None}
        return {
            "data": response,
            "totalCount": 0
        } 
    
    except SQLAlchemyError as e:
        error_message = str(e)
        print("SQLAlchemyError:", error_message) 
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail="Database Error")
    except ValueError as e:
        error_message = str(e)
        print("ValueError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": error_message})
    except Exception as e:
        error_message = str(e)
        print("Exception:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail={"msg": error_message})



async def get_userPartyInfo(
    party_id: int,
    db: AsyncSession
) -> List[dict]:
    try:
        query = (
            select(
                models.User.id, 
                models.User.username, 
                models.UserInfo.gender,
                models.PartyUserInfo.team,
            )
            .join(models.UserInfo, models.User.id == models.UserInfo.user_id, isouter=True)
            .join(models.PartyUserInfo, models.User.id == models.PartyUserInfo.user_id, isouter=True)
            .filter(models.User.party_id == party_id, models.PartyUserInfo.partyOn == True)
            .distinct(models.User.id)  
            .order_by(models.User.id.desc())
        )

        result = await db.execute(query)
        users = result.all()

        response = [
            {
                "id": user.id, 
                "name": user.username,
                "gender": user.gender if user.gender is not None else True,  
                "team": user.team if user.team else None,
            }
            for user in users
        ]
        return {
            "data": response,
            "totalCount": 0
        }
    
    except SQLAlchemyError as e:
        error_message = str(e)
        print("SQLAlchemyError:", error_message) 
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail="Database Error")
    except ValueError as e:
        error_message = str(e)
        print("ValueError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": error_message})
    except Exception as e:
        error_message = str(e)
        print("Exception:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail={"msg": error_message})
    

async def get_userPartyInfoChatExist(
    party_id: int,
    user_id: int,
    db: AsyncSession
) -> List[dict]:
    try:
        query = (
            select(
                models.ChatRoom.id.label("chatRoom_id"),
                models.ChatRoom.user_id_1,
                models.ChatRoom.user_id_2
            )
            .where(
                models.ChatRoom.party_id == party_id, 
                or_(
                    models.ChatRoom.user_id_1 == user_id, 
                    models.ChatRoom.user_id_2 == user_id  
                )
            )
        )

        result = await db.execute(query)
        chatRooms = result.all()

        response = [
            {
                "chatRoom_id": chatRoom.chatRoom_id, 
                "id": chatRoom.user_id_2 if chatRoom.user_id_1 == user_id else chatRoom.user_id_1 
            }
            for chatRoom in chatRooms
        ]
        return {
            "data": response,
            "totalCount": 0
        }
    
    except SQLAlchemyError as e:
        error_message = str(e)
        print("SQLAlchemyError:", error_message) 
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail="Database Error")
    except ValueError as e:
        error_message = str(e)
        print("ValueError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": error_message})
    except Exception as e:
        error_message = str(e)
        print("Exception:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail={"msg": error_message})
    

async def post_userChatRoom(
    db: AsyncSession, 
    userChatRoomRequest: schemas.userChatRoomRequest
):
    try:
        user_id_1 = max(userChatRoomRequest.user_id_1, userChatRoomRequest.user_id_2)
        user_id_2 = min(userChatRoomRequest.user_id_1, userChatRoomRequest.user_id_2)
        
        db_chatRoom = models.ChatRoom(
            user_id_1=user_id_1, 
            user_id_2=user_id_2,
            party_id=userChatRoomRequest.party_id)
        
        db.add(db_chatRoom)
        await db.commit()
        await db.refresh(db_chatRoom)

        query = (
            select(models.ChatRoom.id)
            .where(models.ChatRoom.user_id_1 == user_id_1, 
                   models.ChatRoom.user_id_2 == user_id_2, 
                   models.ChatRoom.party_id == userChatRoomRequest.party_id)
        )
        result = await db.execute(query)
        chatRoom_id = result.scalar_one_or_none()

        response = {"chatRoom_id":chatRoom_id}
        return {
            "data": response,
            "totalCount": 0
        }
        
    except SQLAlchemyError as e:
        error_message = str(e)
        print("SQLAlchemyError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail="Database Error")
    except ValueError as e:
        error_message = str(e)
        print("ValueError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": error_message})
    except Exception as e:
        error_message = str(e)
        print("Exception:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail={"msg": error_message})
    
    

async def post_userChatRooms(
    db: AsyncSession, 
    userChatRoomsRequest: schemas.userChatRoomsRequest
):
    try:
        party_id = userChatRoomsRequest.party_id
        user_id = userChatRoomsRequest.user_id

        query = (
            select(
                models.ChatRoom.id.label("chat_room_id"),
                models.ChatRoom.user_id_1.label("user_id_1"),
                models.ChatRoom.user_id_2.label("user_id_2")
            )
            .where(
                and_(
                    models.ChatRoom.party_id == party_id,
                    or_(
                        models.ChatRoom.user_id_1 == user_id,
                        models.ChatRoom.user_id_2 == user_id
                    )
                )
            )
        )
        
        result = await db.execute(query)
        chat_room_data = result.fetchall()  
        if not chat_room_data:
            return {
                "data": None,
                "totalCount": 0
            }

        response = []
        for chat_room in chat_room_data:
            chat_room_id = chat_room[0]  
            user_id_1 = chat_room[1]  
            user_id_2 = chat_room[2]  


            other_user_id = user_id_1 if user_id != user_id_1 else user_id_2

            user_info_query = (
                select(models.UserInfo.name, models.UserInfo.gender, models.PartyUserInfo.team)
                .join(models.PartyUserInfo, models.PartyUserInfo.user_id == models.UserInfo.user_id)
                .where(models.UserInfo.user_id == other_user_id)
            )
            
            user_info_result = await db.execute(user_info_query)
            user_info = user_info_result.fetchone()

            user_name = user_info[0] if user_info else None
            user_gender = user_info[1] if user_info else None
            user_team = user_info[2] if user_info else None

            latest_chat_query = (
                select(models.Chat.contents, models.Chat.date)
                .join(models.ChatRoom, models.Chat.chatRoom_id == models.ChatRoom.id)
                .where(models.ChatRoom.id == chat_room_id)
                .order_by(models.Chat.date.desc())
            )
            
            latest_chat_result = await db.execute(latest_chat_query)
            latest_chat = latest_chat_result.fetchone()

            chat_contents = latest_chat[0] if latest_chat else ""
            chat_date = latest_chat[1] if latest_chat else ""

            unread_count_query = (
                select(
                    func.count(models.Chat.id).label("unread_count")
                )
                .select_from(models.Chat)
                .join(models.ChatRoom, models.Chat.chatRoom_id == models.ChatRoom.id)
                .join(models.ChatReadStatus, models.ChatRoom.id == models.ChatReadStatus.chatRoom_id)
                .where(models.ChatReadStatus.user_id == user_id)
                .where(
                    case(
                        (models.ChatReadStatus.lastReadChat_id.is_(None), True),  
                        (models.Chat.id > models.ChatReadStatus.lastReadChat_id, True),  
                        else_=False  
                    )
                )
                .where(models.ChatRoom.id == chat_room_id)
                .where(models.Chat.user_id != user_id)
            )

            
            unread_count_result = await db.execute(unread_count_query)
            unread_count = unread_count_result.scalar()

            response.append({
                "id": chat_room_id,
                "user_id_2": other_user_id,
                "gender": user_gender,
                "team": user_team,
                "name": user_name,
                "contents": chat_contents,
                "date": chat_date,
                "unreadCount": unread_count,
            })

        return {
            "data": response,
            "totalCount": len(response)
        }

    except SQLAlchemyError as e:
        error_message = str(e)
        print("SQLAlchemyError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail="Database Error")
    except ValueError as e:
        error_message = str(e)
        print("ValueError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": error_message})
    except Exception as e:
        error_message = str(e)
        print("Exception:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail={"msg": error_message})



async def post_userChatContents(
    db: AsyncSession, 
    userChatContentsRequest: schemas.userChatContentsRequest,
):
    try:
        chatRoom_id = userChatContentsRequest.chatRoom_id
        lastChat_id = userChatContentsRequest.lastChat_id 
        
        if lastChat_id is None:
            query = (
                select(models.Chat)
                .where(models.Chat.chatRoom_id == chatRoom_id)
                .order_by(models.Chat.id.desc())
                .limit(30)
            )
        else:
            query = (
                select(models.Chat)
                .where(
                    models.Chat.chatRoom_id == chatRoom_id,
                    models.Chat.id < lastChat_id  
                )
                .order_by(models.Chat.id.desc())
                .limit(30)
            )
        
        result = await db.execute(query)
        chat_room_datas = result.fetchall()  

        response = [{
                "id": chat_room_data[0].id,
                "user_id": chat_room_data[0].user_id,
                "contents": chat_room_data[0].contents,
                "date": chat_room_data[0].date
                } for chat_room_data in chat_room_datas   
            ]

        response.reverse()
        
        return {
            "data": response,
            "totalCount": 0
        }
        
    except SQLAlchemyError as e:
        error_message = str(e)
        print("SQLAlchemyError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail="Database Error")
    except ValueError as e:
        error_message = str(e)
        print("ValueError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": error_message})
    except Exception as e:
        error_message = str(e)
        print("Exception:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail={"msg": error_message})


# class ConnectionManager:
#     def __init__(self):
#         self.chat_room_connections: Dict[int, Dict[int, WebSocket]] = {}
#         self.lock = asyncio.Lock() 

#     async def connect(self, websocket: WebSocket, chatRoom_id: int, user_id: int):
#         await websocket.accept()
#         async with self.lock:
#             if chatRoom_id not in self.chat_room_connections:
#                 self.chat_room_connections[chatRoom_id] = {}
#             self.chat_room_connections[chatRoom_id][user_id] = websocket

#     async def disconnect(self, chatRoom_id: int, user_id: int):
#         async with self.lock:
#             if chatRoom_id in self.chat_room_connections:
#                 if user_id in self.chat_room_connections[chatRoom_id]:
#                     del self.chat_room_connections[chatRoom_id][user_id]
                
#                 if not self.chat_room_connections[chatRoom_id]:
#                     del self.chat_room_connections[chatRoom_id]

#     async def broadcast(self, message: str, chatRoom_id: int):
#         if chatRoom_id not in self.chat_room_connections:
#             return
#         to_remove = []

#         async with self.lock:
#             connections = list(self.chat_room_connections[chatRoom_id].items())
        
#         async def send_message(user_id, connection):
#             try:
#                 await connection.send_text(message)
#             except Exception:
#                 to_remove.append(user_id)
        
#         await asyncio.gather(*(send_message(user_id, connection) for user_id, connection in connections))

#         async with self.lock:
#             for user_id in to_remove:
#                 if user_id in self.chat_room_connections.get(chatRoom_id, {}):
#                     del self.chat_room_connections[chatRoom_id][user_id]

#             if not self.chat_room_connections.get(chatRoom_id):
#                 del self.chat_room_connections[chatRoom_id]

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}
        self.lock = asyncio.Lock()

    async def connect(self, chatRoom_id: int, websocket: WebSocket):
        await websocket.accept()
        async with self.lock:
            if chatRoom_id not in self.active_connections:
                self.active_connections[chatRoom_id] = []
            
            if len(self.active_connections[chatRoom_id]) >= 2:
                await websocket.close()
                return 
            self.active_connections[chatRoom_id].append(websocket)

    async def disconnect(self, chatRoom_id: int, websocket: WebSocket):
        async with self.lock:
            self.active_connections[chatRoom_id].remove(websocket)
            if not self.active_connections[chatRoom_id]:
                del self.active_connections[chatRoom_id]
                
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, chatRoom_id: int, message: str):
        connections = self.active_connections.get(chatRoom_id, [])
        for connection in connections[:]:  
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"WebSocket 전송 오류: {e}")
                await self.disconnect(chatRoom_id, connection)
                
manager = ConnectionManager()


async def post_chat(
    db: AsyncSession, 
    chat: schemas.chatCreateRequest,
):
    try:
        db_chat = models.Chat(user_id=chat.user_id, contents=chat.contents, chatRoom_id=chat.chatRoom_id, date=format_dates(datetime.now()))
        db.add(db_chat)
        await db.commit()
        await db.refresh(db_chat)
        
        await manager.broadcast(f"User {chat.user_id} says: {chat.contents}", chat.chatRoom_id)
        return {"msg": "Chat created successfully"}
        
    except SQLAlchemyError as e:
        error_message = str(e)
        print("SQLAlchemyError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail="Database Error")
    except ValueError as e:
        error_message = str(e)
        print("ValueError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": error_message})
    except Exception as e:
        error_message = str(e)
        print("Exception:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail={"msg": error_message})
    
    
async def get_chatId(
    db: AsyncSession,
    chatRoom_id: int,
    user_id: int
):
    try:
        query = (
            select(models.Chat.id)
            .where(models.Chat.chatRoom_id == chatRoom_id, models.Chat.user_id == user_id)
            .order_by(models.Chat.id.desc())
            .limit(1)
        )
        result = await db.execute(query)
        existing_chat_id = result.scalar_one_or_none()
        
        return existing_chat_id  
        
    except SQLAlchemyError as e:
        error_message = str(e)
        print("SQLAlchemyError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail="Database Error")
    except ValueError as e:
        error_message = str(e)
        print("ValueError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": error_message})
    except Exception as e:
        error_message = str(e)
        print("Exception:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail={"msg": error_message})
    
async def post_lastReadChat(
    db: AsyncSession, 
    chat: schemas.chatCreateRequest,
):
    try:
        chatRoom_id = chat.chatRoom_id
        user_id = chat.user_id
        lastReadChat_id=chat.lastReadChat_id
        
        query = (
            select(
                models.ChatReadStatus
            )
            .where(
                and_(
                    models.ChatReadStatus.chatRoom_id == chatRoom_id,
                    models.ChatReadStatus.user_id == user_id
                )
            )
        )
        
        result = await db.execute(query)
        existing_chat_status = result.scalar_one_or_none()

        if existing_chat_status:
            existing_chat_status.lastReadChat_id = lastReadChat_id
            existing_chat_status.date = format_dates(datetime.now())
            msg = "ChatReadStatus updated successfully"
        
        else:
            db_chat = models.ChatReadStatus(
                chatRoom_id=chatRoom_id, 
                user_id=user_id, 
                lastReadChat_id=lastReadChat_id, 
                date=format_dates(datetime.now())
            )
            db.add(db_chat)
            msg = "ChatReadStatus created successfully"

        await db.commit()
        return {"msg": msg}
        
    except SQLAlchemyError as e:
        error_message = str(e)
        print("SQLAlchemyError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail="Database Error")
    except ValueError as e:
        error_message = str(e)
        print("ValueError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": error_message})
    except Exception as e:
        error_message = str(e)
        print("Exception:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail={"msg": error_message})
    

async def get_userMatchUserList(
    userList: schemas.userMatchUserListRequest,
    db: AsyncSession
) -> List[dict]:
    try:
        party_id = userList.party_id
        user_id = userList.user_id

        subquery = (
            select(models.PartyUserInfo.team)
            .filter(models.PartyUserInfo.user_id == user_id)
            .scalar_subquery()
        )

        query = (
            select(
                models.User.id, 
                models.UserInfo.name, 
                models.UserInfo.gender,
                models.PartyUserInfo.team,
            )
            .join(models.UserInfo, models.User.id == models.UserInfo.user_id, isouter=True)
            .join(models.PartyUserInfo, models.User.id == models.PartyUserInfo.user_id, isouter=True)
            .filter(
                models.User.party_id == party_id,  
                models.PartyUserInfo.partyOn == True,
                models.PartyUserInfo.team == subquery 
            )
            .distinct(models.User.id)
            .order_by(models.User.id.desc())
        )

        result = await db.execute(query)
        users = result.all()

        response = [
            {
                "id": user.id, 
                "name": user.name,
                "gender": user.gender if user.gender is not None else True,  
                "team": user.team if user.team else None,
            }
            for user in users
        ]
        return {
            "data": response,
            "totalCount": 0
        }
    
    except SQLAlchemyError as e:
        error_message = str(e)
        print("SQLAlchemyError:", error_message) 
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail="Database Error")
    except ValueError as e:
        error_message = str(e)
        print("ValueError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": error_message})
    except Exception as e:
        error_message = str(e)
        print("Exception:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail={"msg": error_message})

async def post_userMatchSelect(
    db: AsyncSession, 
    userChatRoomRequest: schemas.userChatRoomRequest
):
    try:
        db_matchSelect = models.UserMatch(
            user_id_1=userChatRoomRequest.user_id_1, 
            user_id_2=userChatRoomRequest.user_id_2,
            party_id=userChatRoomRequest.party_id,
            date=format_dates(datetime.now()))
        
        db.add(db_matchSelect)
        await db.commit()
        await db.refresh(db_matchSelect)

        return {"msg": "ChatRoom created successfully"}
        
    except SQLAlchemyError as e:
        error_message = str(e)
        print("SQLAlchemyError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail="Database Error")
    except ValueError as e:
        error_message = str(e)
        print("ValueError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": error_message})
    except Exception as e:
        error_message = str(e)
        print("Exception:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail={"msg": error_message})
    

async def get_userMatchConfirm(
    party_id: int,
    user_id: int,
    db: AsyncSession
) -> List[dict]:
    try:
        query = (
            select(models.UserMatch.user_id_2)
            .where(models.UserMatch.party_id == party_id, models.UserMatch.user_id_1 == user_id))

        result = await db.execute(query)
        user_id_2 = result.scalar_one_or_none()


        response = {
            "user_id_2": user_id_2
        }

        return response
    
    except SQLAlchemyError as e:
        error_message = str(e)
        print("SQLAlchemyError:", error_message) 
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail="Database Error")
    except ValueError as e:
        error_message = str(e)
        print("ValueError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": error_message})
    except Exception as e:
        error_message = str(e)
        print("Exception:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail={"msg": error_message})
    
    
async def get_userMatchSelect(
    party_id: int,
    db: AsyncSession
) -> List[dict]:
    try:
        UserInfo_1 = aliased(models.UserInfo)
        UserInfo_2 = aliased(models.UserInfo)

        query = (
            select(
                models.UserMatch.user_id_1,
                models.UserMatch.user_id_2,
                UserInfo_1.phone.label("man_phone"), 
                UserInfo_1.name.label("man_name"),    
                UserInfo_2.phone.label("woman_phone"), 
                UserInfo_2.name.label("woman_name"),    
                UserInfo_1.gender,
                models.PartyUserInfo.team
            )
            .where(models.UserMatch.party_id == party_id)
            .join(
                UserInfo_1, models.UserMatch.user_id_1 == UserInfo_1.user_id  
            )
            .join(
                UserInfo_2, models.UserMatch.user_id_2 == UserInfo_2.user_id 
            )
            .join(
                models.PartyUserInfo,
                UserInfo_1.user_id == models.PartyUserInfo.user_id
            )
        )
            

        result = await db.execute(query)
        matchSelect = result.all()

        data = []
        seen_pairs = set()
        valid_pairs = set()

        match_dict = {}
        for row in matchSelect:
            user_pair = tuple(sorted([row.user_id_1, row.user_id_2]))
            if user_pair in match_dict:
                valid_pairs.add(user_pair)
            else:
                match_dict[user_pair] = True

        for row in matchSelect:
            user_pair = tuple(sorted([row.user_id_1, row.user_id_2]))
            
            if user_pair not in valid_pairs:
                continue 
            
            if user_pair in seen_pairs:
                continue
            
            seen_pairs.add(user_pair)
            
            if row.gender:  
                man_user_id, woman_user_id = user_pair
                man_name, man_phone = row.man_name, row.man_phone
                woman_name, woman_phone = row.woman_name, row.woman_phone
            else:  
                woman_user_id, man_user_id = user_pair
                woman_name, woman_phone = row.man_name, row.man_phone
                man_name, man_phone = row.woman_name, row.woman_phone
            
            data.append({
                "man": {
                    "user_id": man_user_id,
                    "name": man_name,
                    "phone": man_phone,
                    "team": row.team
                },
                "woman": {
                    "user_id": woman_user_id,
                    "name": woman_name,
                    "phone": woman_phone,
                    "team": row.team
                }
            })

        response = {
            "data": data if data else None, 
            "totalCount": len(data)  
        }

        return response
    
    except SQLAlchemyError as e:
        error_message = str(e)
        print("SQLAlchemyError:", error_message) 
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail="Database Error")
    except ValueError as e:
        error_message = str(e)
        print("ValueError:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": error_message})
    except Exception as e:
        error_message = str(e)
        print("Exception:", error_message)
        await log_error(db, error_message)
        raise HTTPException(status_code=500, detail={"msg": error_message})
