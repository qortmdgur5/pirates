import os
from typing import List, Optional
from urllib.parse import urlencode
from fastapi import HTTPException
from sqlalchemy import func, select, desc, asc, and_
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils import models, schemas
from ..utils.utils import load_config
from datetime import datetime, timedelta, timezone, time
from ..oauth.password import hash_password, verify_password
import qrcode
import logging
from sqlalchemy.exc import SQLAlchemyError
from operator import itemgetter
from itertools import groupby

config = load_config("config.yaml")

logging.basicConfig(
    level=logging.ERROR, 
    format="%(asctime)s - %(levelname)s - %(message)s",
     handlers=[
        logging.FileHandler("app_errors.log"),  
        logging.StreamHandler()  
    ])
logger = logging.getLogger("uvicorn.access")

async def log_error(db: AsyncSession, message: str):
    try:
        logging.error(f"Error: {message}") 
        error_log = models.ErrorLog(message=message)
        db.add(error_log)
        await db.commit()
    except Exception as log_error:
        print(f"Error while logging: {log_error}")
        logging.error(f"Error while logging to DB: {log_error}")
        
        
def format_date(date_obj):
    kst_date = date_obj + timedelta(hours=9)
    return kst_date.strftime("%y.%m.%d")

def format_dates(date_obj):
    kst_tz = timezone(timedelta(hours=9))
    return date_obj.astimezone(kst_tz)

def format_party_time(party_time: str) -> str:
    time_obj = datetime.combine(datetime.today(), party_time)
    return time_obj.strftime('%I:%M %p') 



## admin (관리자 사용 API)
async def get_adminAccomodations(
    db: AsyncSession,
    isMostReviews: Optional[bool] = False,
    page: int = 0,
    pageSize: int = 10
) -> List[dict]:
    try:
        query = select(models.Accomodation)
        if isMostReviews:
            query = query.outerjoin(models.Review)
            query = query.group_by(models.Accomodation.id)
            query = query.add_columns(func.count(models.Review.id).label("review_count"))
            query = query.order_by(desc("review_count"))
        else:
            query = query.order_by(models.Accomodation.date.desc())
        
        offset = max(page * pageSize, 0)
        query = query.offset(offset).limit(pageSize)
        
        totalCount_query = select(func.count()).select_from(models.Accomodation)
        totalCount = await db.scalar(totalCount_query)
        
        result = await db.execute(query)
        accomodations = result.scalars().all()
        
        response = [
            {
                "id": accomodation.id,
                "name": accomodation.name,
                "address": accomodation.address,
                "number": accomodation.number,
                "date": format_date(accomodation.date) if accomodation.date else None
            }
            for accomodation in accomodations
        ]
        
        return  {
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
    
async def get_adminOwners(
    db: AsyncSession, 
    isOldestOrders: Optional[bool] = False, 
    page: int = 0, 
    pageSize: int = 10
):
    try:
        offset = max(page * pageSize, 0)
        query = select(
            models.Owner.id,
            models.Owner.name,
            models.Owner.username,
            models.Owner.phoneNumber,
            models.Owner.role
        ).order_by(models.Owner.date if isOldestOrders else desc(models.Owner.date))\
         .offset(offset).limit(pageSize)
         
        totalCount_query = select(func.count()).select_from(models.Owner)
        totalCount = await db.scalar(totalCount_query)
        
        result = await db.execute(query)
        owners = result.all()
        
        response = [
            {
                "id": owner.id,
                "name": owner.name,
                "username": owner.username,
                "phoneNumber": owner.phoneNumber,
                "isAuth": True if owner.role == "ROLE_AUTH_OWNER" else False
            }
            for owner in owners
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
    
async def put_auth_adminOwners(db: AsyncSession, id: int):
    
    result = await db.execute(
        select(models.Owner).filter(models.Owner.id == id)
    )
    db_owner = result.scalar_one_or_none()
    if db_owner:
        try:
            db_owner.role = "ROLE_AUTH_OWNER"
            await db.commit()
            await db.refresh(db_owner)
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


async def put_deny_adminOwners(db: AsyncSession, id: int):
    result = await db.execute(
        select(models.Owner).filter(models.Owner.id == id)
    )
    db_owner = result.scalar_one_or_none()
    if db_owner:
        try:
            db_owner.role = "ROLE_NOTAUTH_OWNER"
            await db.commit()
            await db.refresh(db_owner)
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




## owner (사장님 사용 API)
async def create_signup_owner(db: AsyncSession, data: schemas.signupOwner):
    try:
        db_owner = models.Owner(
            username=data.username,
            password=hash_password(data.password),
            role="ROLE_NOTAUTH_OWNER",
            name=data.name,
            phoneNumber=data.phoneNumber,
            date=format_dates(datetime.now()),
        )
        db.add(db_owner)
        await db.commit()
        await db.refresh(db_owner)
        
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

async def create_duplicate_owner(db: AsyncSession, username: str):
    try:
        query = await db.execute(select(models.Owner).where(models.Owner.username == username))
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


async def authenticate_owner(db: AsyncSession, username: str, password: str):
    try:
        query = (
            select(models.Owner, models.Accomodation)
            .join(models.Accomodation, models.Accomodation.owner_id == models.Owner.id, isouter=True)
            .filter(models.Owner.username == username)
        )
        
        result = await db.execute(query)
        row = result.first() 

        if not row:
            raise HTTPException(status_code=404, detail="Owner not found")

        owner, accomodation = row

        pw = verify_password(password, owner.password)

        accomodation_id = accomodation.id if accomodation else None
        
        return owner, pw, accomodation_id
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

async def get_ownerAccomodation(
    id: int,
    db: AsyncSession,
    page: int = 0,
    pageSize: int = 10
) -> List[dict]:
    try:
        offset = max(page * pageSize, 0)
        
        query = (
            select(models.Accomodation)
            .filter(models.Accomodation.owner_id == id) 
            .order_by(asc(models.Accomodation.date))
            .offset(offset)
            .limit(pageSize)
        )

        totalCount_query = select(func.count()).select_from(models.Accomodation).filter(models.Accomodation.owner_id == id)
        totalCount = await db.scalar(totalCount_query)
        
        result = await db.execute(query)
        accomodations = result.scalars().all()
        
        response = [
                {
                    "id": accomodation.id,
                    "name": accomodation.name,
                    "address": accomodation.address,
                    "number": accomodation.number,
                    "introduction": accomodation.introduction,
                    "score": accomodation.score,
                    "loveCount": accomodation.loveCount
                }
                for accomodation in accomodations
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

async def post_ownerAccomodation(db: AsyncSession, accomodation: schemas.OwnerAccomodationsPost):
    try:
        qr_directory = config['qr_directory']
        os.makedirs(qr_directory, exist_ok=True)
        
        base_url = config['qr_code']  
        query_params = {
            "id": accomodation.id
        }
        full_url = f"{base_url}?{urlencode(query_params)}"
        
        qr_img = qrcode.make(full_url)
        qr_filename = f"{accomodation.id}_{accomodation.name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        qr_path = os.path.join(qr_directory, qr_filename)
        qr_img.save(qr_path) 
        
        db_accomodation = models.Accomodation(
            owner_id=accomodation.id,
            name=accomodation.name,
            address=accomodation.address,
            introduction=accomodation.introduction,
            number=accomodation.number,
            date = format_dates(datetime.now()),
            directory = qr_path 
        )
        db.add(db_accomodation)
        await db.commit()
        await db.refresh(db_accomodation)
        
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

async def put_ownerAccomodation(db: AsyncSession, id: int, accomodation: schemas.OwnerAccomodationsPut):
    
    result = await db.execute(
        select(models.Accomodation).filter(models.Accomodation.id == id)
    )
    db_accomodation = result.scalar_one_or_none()
    if db_accomodation:
        try:
            db_accomodation.name = accomodation.name
            db_accomodation.address = accomodation.address
            db_accomodation.number = accomodation.number
            db_accomodation.introduction = accomodation.introduction
            db_accomodation.date = format_dates(datetime.now())
            
            await db.commit()
            await db.refresh(db_accomodation)
            
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


async def get_ownermanagers(
    id: int,
    db: AsyncSession,
    isOldestOrders: Optional[bool] = False,
    page: int = 0,
    pageSize: int = 10
) -> List[dict]:
    try:
        offset = max(page * pageSize, 0)

        query = select(models.Manager).filter(models.Manager.owner_id == id)

        query = query.offset(offset).limit(pageSize)

        query = query.order_by(asc(models.Manager.id) if isOldestOrders else desc(models.Manager.id))

        totalCount_query = select(func.count()).select_from(models.Manager).filter(models.Manager.owner_id == id)
        totalCount = await db.scalar(totalCount_query)

        result = await db.execute(query)
        managers = result.scalars().all()
        
        response = [
                {
                    "id": manager.id,
                    "name": manager.name,
                    "username": manager.username,
                    "phoneNumber": manager.phoneNumber,
                    "date": format_date(manager.date),
                    "isAuth": True if manager.role == "ROLE_AUTH_MANAGER" else False 
                }
                for manager in managers
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



async def put_auth_ownerOwners(db: AsyncSession, id: int):
    result = await db.execute(
        select(models.Manager).filter(models.Manager.id == id)
    )
    db_manager = result.scalar_one_or_none()
    if db_manager:
        try:
            db_manager.role = "ROLE_AUTH_MANAGER"
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
    else:
        return {"msg": "fail"}

async def put_deny_ownerOwners(db: AsyncSession, id: int):
    result = await db.execute(
        select(models.Manager).filter(models.Manager.id == id)
    )
    db_manager = result.scalar_one_or_none()
    if db_manager:
        try:
            db_manager.role = "ROLE_NOTAUTH_MANAGER"
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
    else:
        return {"msg": "fail"}


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
    


