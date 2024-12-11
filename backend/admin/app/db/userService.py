from sqlalchemy import func, select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from .errorLog import log_error
from ..utils import models, schemas
from typing import List, Optional
from datetime import datetime, timedelta, timezone, time
from operator import itemgetter
from itertools import groupby

## user
## 카카오 로그인 
## qr api -> "/user/auth/kakao/login" -> 채팅방 url 이동 api 
def get_kst_now():
    return datetime.now(timezone(timedelta(hours=9)))

async def post_userLoginKakaoCallback(
    db: AsyncSession, 
    user_info: dict,
    accomodation_id: int
):
    try:
        username = user_info.get("id")
        nickname = user_info.get("properties", {}).get("nickname")

        existing_user = await db.execute(
            select(models.User).where(models.User.username == username)
        )
        user = existing_user.scalars().first()

        if not user:
            kst_now = get_kst_now()  
            current_time = kst_now.time()  
            today_kst = kst_now.date()  
            yesterday_kst = today_kst - timedelta(days=1) 

            if current_time >= time(hour=0) and current_time < time(hour=6):
                query_date = yesterday_kst  
            else:
                query_date = today_kst

            query_accomodation = (
                select(
                    models.Party.id,
                    )
                    .where(
                        and_(
                            models.Party.accomodation_id == accomodation_id,
                            models.Party.partyDate == query_date
                        )
                    )
            )

            result_party = await db.execute(query_accomodation)
            party_id = result_party.scalar()


            new_user = models.User(username=username, party_id=party_id, nickname=nickname)
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)

            query = (
                select(
                    models.User.id,
                    )
                    .where(models.User.username == username)
                )

            result = await db.execute(query)
            users = result.all()

            
            grouped_data = [{
                "id": new_user.id,
                "party_id": party_id,
                "userInfo": []
                }]

            return {
                    "data": grouped_data,
                    "totalCount": 0
                } 

        else:
            query = (
            select(
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
            )
                .join(models.UserInfo, models.UserInfo.user_id == models.User.id)
                .where(models.User.username == username)
            )

            result = await db.execute(query)
            rows = result.all()

            grouped_data = []
            rows_sorted = sorted(rows, key=itemgetter(0, 1))
            for (user_id, party_id), group in groupby(rows_sorted, key=itemgetter(0, 1)): 
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
                    for info in group
                ]
                grouped_data.append({
                    "id": user_id,
                    "party_id": party_id,
                    "userInfo": user_info_list,
                })
            return {
                "data": grouped_data,
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
                models.Party.partyOn
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
                    "party_on": party.partyOn
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

async def get_userPartyInto(
    id: int,
    db: AsyncSession,
    page: int = 0,
    pageSize: int = 10
) -> List[dict]:
    try:
        offset = max(page * pageSize, 0)
        query = (
            select(models.User, models.UserInfo, models.PartyUserInfo, models.Party)
            .join(models.UserInfo, models.User.id == models.UserInfo.user_id, isouter=True)
            .join(models.Party, models.Party.id == models.User.party_id, isouter=True)
            .join(models.PartyUserInfo, models.User.id == models.PartyUserInfo.user_id, isouter=True)
            .filter(models.User.party_id == id, models.Party.partyOn == True)
            .order_by(models.User.id.desc())
            .offset(offset)  
            .limit(pageSize)
        )

        result = await db.execute(query)
        users = result.all()
        
        totalCount_query = (
            select(func.count(models.User.id))
            .filter(models.User.party_id == id)
        )
        totalCount = await db.scalar(totalCount_query)
        response = [
                {
                    "id": user[0].id, 
                    "name": user[0].username,
                    "gender": user[1].gender if user[1] else None,
                    "team": user[2].team if user[2] else None
                }
                for user in users
            ]
        return {
            "data": response,
            "totalCount": totalCount
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
    


