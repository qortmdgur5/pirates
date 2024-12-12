import os
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from .errorLog import format_date, log_error, format_dates, format_party_time
from ..utils import models, schemas
from typing import List, Optional
from datetime import datetime
from ..oauth.password import hash_password, verify_password

## owner , manager(사장님 And 매니저 사용 API)
async def get_managerGetAccomodation(
    db: AsyncSession,
) -> List[dict]:
    try:
        query = (
            select(models.Accomodation.owner_id, models.Accomodation.name)
            .order_by(models.Accomodation.name.asc())
        )

        result = await db.execute(query)
        managerAccomodations = result.all()
        
        response = [
            {
                "owner_id": managerAccomodation.owner_id,
                "accomodationName": managerAccomodation.name
            }
            for managerAccomodation in managerAccomodations
        ]
        
        return {
            "data": response
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
    
    
async def create_signup_mananger(db: AsyncSession, data: schemas.signupManager):
    try:
        db_manager = models.Manager(
            owner_id=data.owner_id,
            username=data.username,
            password=hash_password(data.password),
            role="ROLE_NOTAUTH_OWNER",
            name=data.name,
            phoneNumber=data.phoneNumber,
            date=format_dates(datetime.now()),
        )
        db.add(db_manager)
        await db.commit()
        await db.refresh(db_manager)
        
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

async def create_duplicate_mananger(db: AsyncSession, username: str):
    try:
        query = await db.execute(select(models.Manager).where(models.Manager.username == username))
        result = query.scalars().one_or_none()

        is_duplicate = result is not None
        return {"duplicate": is_duplicate}
    
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


async def authenticate_mananger(db: AsyncSession, username: str, password: str):
    try:
        query = (
            select(models.Manager, models.Accomodation)
            .outerjoin(models.Accomodation, models.Accomodation.owner_id == models.Manager.id)
            .filter(models.Manager.username == username)
        )
        
        result = await db.execute(query)
        row = result.first() 
        
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        
        user, accomodation = row
        
        pw = verify_password(password, user.password)

        accomodation_id = accomodation.id if accomodation else None
        
        return user, pw, accomodation_id
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
    
async def get_managerParties(
    id: int,
    db: AsyncSession,
    isOldestOrders: Optional[bool] = False,
    page: int = 0,
    pageSize: int = 10
) -> List[dict]:
    try:
        offset = max(page * pageSize, 0)
        order_by_field = models.Party.partyDate.asc() if isOldestOrders else models.Party.partyDate.desc()

        query = (
            select(
                models.Party.id,
                models.Party.partyDate,
                models.Party.number,
                models.Party.partyOpen,
                models.Party.partyTime,
                func.count(models.Participant.id).label("participant_count")
            )
            .join(models.Participant, models.Party.id == models.Participant.party_id, isouter=True)
            .filter(models.Party.accomodation_id == id)
            .group_by(models.Party.id)
            .order_by(order_by_field)
            .offset(offset)  
            .limit(pageSize)
        )
        
        result = await db.execute(query)
        managerParties = result.all()
        
        totalCount_query = (
            select(func.count(models.Party.id))
            .filter(models.Party.accomodation_id == id)
        )
        totalCount = await db.scalar(totalCount_query)

        response = [
            {
                "id": managerParty.id,
                "partyDate": format_date(managerParty.partyDate),
                "number": managerParty.number,
                "partyOpen": managerParty.partyOpen,
                "partyTime": format_party_time(managerParty.partyTime),
                "participant": managerParty.participant_count  
            }
            for managerParty in managerParties
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



async def post_managerParty(db: AsyncSession, party: schemas.managerPartiesPost):
    try:
        formatted_date = datetime.strptime(party.partyDate, "%Y-%m-%d")
        formatted_time = datetime.strptime(party.partyTime, "%H-%M-%S").time()
        
        db_party = models.Party(
            accomodation_id=party.id,
            partyDate=formatted_date,
            number=party.number,
            partyOpen=party.partyOpen,
            partyTime=formatted_time
        )
        db.add(db_party)
        await db.commit()
        await db.refresh(db_party)
        
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

async def put_managerParty(db: AsyncSession, id: int, party: schemas.managerParties):
    result = await db.execute(
        select(models.Party).filter(models.Party.id == id)
    )
    
    db_party = result.scalar_one_or_none()
    if db_party:
        try:
            formatted_date = datetime.strptime(party.partyDate, "%Y-%m-%d")
            formatted_time = datetime.strptime(party.partyTime, "%H-%M-%S").time()
            
            db_party.partyDate = formatted_date
            db_party.number = party.number
            db_party.partyOpen = party.partyOpen
            db_party.partyTime = formatted_time
            await db.commit()
            await db.refresh(db_party)
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
    else:
        return {"msg": "fail"}
    
async def del_managerParty(db: AsyncSession, id: int):
    result = await db.execute(
        select(models.Party).filter(models.Party.id == id)
    )
    
    db_party = result.scalar_one_or_none()
    if db_party:
        try:
            await db.delete(db_party) 
            await db.commit() 
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
    else:
        return {"msg": "fail"}
    
    
async def get_managerParty(
    id: int,
    db: AsyncSession,
    page: int = 0,
    pageSize: int = 10
) -> List[dict]:
    try:
        offset = max(page * pageSize, 0)
        query = (
            select(models.Participant)
            .filter(models.Participant.party_id == id)
            .order_by(models.Participant.id.desc())
            .offset(offset)  
            .limit(pageSize)
        )

        result = await db.execute(query)
        participants = result.scalars().all()

        totalCount_query = (
            select(func.count(models.Participant.id))
            .filter(models.Participant.party_id == id)
        )
        totalCount = await db.scalar(totalCount_query)
        response = [
            {
                "id": participant.id,
                "name": participant.name,
                "phone": participant.phone,
                "age": participant.age,
                "gender": "남자" if participant.gender else "여자",
                "mbti": participant.mbti,
                "region": participant.region
            }
            for participant in participants
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
    
async def post_managerParticipant(db: AsyncSession, participants: schemas.managerParticipantPost):
    try:
        db_participant = models.Participant(
            party_id=participants.id,
            name=participants.name,
            phone=participants.phone,
            age=participants.age,
            gender=participants.gender,
            mbti=participants.mbti,
            region=participants.region
        )
        db.add(db_participant)
        await db.commit()
        await db.refresh(db_participant)
        
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


    
async def del_managerParticipant(db: AsyncSession, id: int):
    result = await db.execute(
        select(models.Participant).filter(models.Participant.id == id)
    )
    
    db_participant = result.scalar_one_or_none()
    if db_participant:
        try:
            await db.delete(db_participant) 
            await db.commit() 
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
    else:
        return {"msg": "fail"}
    
    
async def put_managerPartyOn(db: AsyncSession, id: int, party: schemas.managerPartyOn):
    result = await db.execute(
        select(models.Party).filter(models.Party.id == id)
    )
    
    db_party = result.scalar_one_or_none()
    if db_party:
        try:
            db_party.partyOn = party.partyOn
            await db.commit()
            await db.refresh(db_party)
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
    else:
        return {"msg": "fail"}
    
async def get_managerAccomodationQR(
    id: int,
    db: AsyncSession
) -> str:
    try:
        query = select(models.Accomodation).filter(models.Accomodation.id == id)
        result = await db.execute(query)
        accomodation = result.scalar_one_or_none()

        if not accomodation:
            raise HTTPException(status_code=404, detail="Accommodation not found")
        
        qr_code_path = accomodation.directory
        if not qr_code_path or not os.path.exists(qr_code_path):
            raise HTTPException(status_code=404, detail="QR code file not found")
        
        return qr_code_path
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


async def get_managerPartyInfo(
    id: int,
    db: AsyncSession
) -> List[dict]:
    try:
        query = (
            select(models.User, models.UserInfo, models.PartyUserInfo, models.Party)
            .join(models.UserInfo, models.User.id == models.UserInfo.user_id, isouter=True)
            .join(models.Party, models.Party.id == models.User.party_id, isouter=True)
            .join(models.PartyUserInfo, models.User.id == models.PartyUserInfo.user_id, isouter=True)
            .order_by(models.User.id.desc())
        )

        result = await db.execute(query)
        users = result.all()
        
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


async def put_managerPartyInfo(db: AsyncSession, data: schemas.managerPartyUserInfoDatas):
    try:
        updated_count = 0

        for item in data.data:
            user_id, team = item.id, item.team

            result = await db.execute(
                select(models.PartyUserInfo)
                .where(models.PartyUserInfo.user_id == user_id)
            )
            db_party = result.scalar_one_or_none()

            if db_party is None:
                print(f"No record found for user_id={user_id}. Skipping.")
                continue

            if db_party.team != team:
                print(f"Updating team for user_id={user_id} from {db_party.team} to {team}.")
                db_party.team = team
                updated_count += 1

            await db.commit()
            await db.refresh(db_party)

        return {
            "msg": "ok",
            "updated_count": updated_count,
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
