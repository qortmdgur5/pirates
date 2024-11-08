import os
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import func, select, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils import models, schemas
from ..utils.utils import load_config
from datetime import datetime, timedelta, timezone
from ..oauth.password import hash_password, pwd_context, get_password_hash, verify_password
import qrcode
import logging
import time
from sqlalchemy.exc import SQLAlchemyError

config = load_config("config.yaml")

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def log_error(db: AsyncSession, message: str):
    try:
        logging.error(f"Error: {message}") 
        error_log = models.ErrorLog(message=message)
        db.add(error_log)
        await db.commit()
    except Exception as log_error:
        print(f"Error while logging: {log_error}")
        
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
        
        offset = max((page - 1) * pageSize, 0)
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
        offset = max((page - 1) * pageSize, 0)
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
        owner, accomodation = result.scalar_one_or_none()

        if not owner:
            raise HTTPException(status_code=404, detail="Owner not found")

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
        offset = max((page - 1) * pageSize, 0)
        
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
        qr_directory = "/home/qr_directory"
        os.makedirs(qr_directory, exist_ok=True)
        
        qr_data = config['qr_code']
        
        qr_img = qrcode.make(qr_data)
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
        offset = max((page - 1) * pageSize, 0)

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
    page: int = 0,
    pageSize: int = 10
) -> List[dict]:
    try:
        offset = max((page - 1) * pageSize, 0)
        
        query = (
            select(models.Accomodation.owner_id, models.Accomodation.name)
            .order_by(models.Accomodation.owner_id)
            .offset(offset)
            .limit(pageSize)
        )

        totalCount = await db.scalar(select(func.count()).select_from(models.Accomodation))

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
        user, accomodation = result.scalar_one_or_none()  
        
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
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
        offset = max((page - 1) * pageSize, 0)
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
            .join(models.Participant, models.Party.id == models.Participant.party_id, isouter=True)
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
        query = (
            select(models.Participant)
            .filter(models.Participant.party_id == id)
            .order_by(models.Participant.id.desc())
            .offset((page - 1) * pageSize)  
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