
from typing import List, Optional
from sqlalchemy import func, select, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils import models
from ..utils import schemas
from ..service.admin import hash_password
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

async def log_error(db: AsyncSession, message: str):
    error_log = models.ErrorLog(message=message)
    db.add(error_log)
    await db.commit()

def format_date(date_obj):
    kst_date = date_obj + timedelta(hours=9)
    return kst_date.strftime("%y.%m.%d")

def format_dates(date_obj):
    kst_tz = timezone(timedelta(hours=9))
    return date_obj.astimezone(kst_tz)

def format_party_time(party_time: str) -> str:
    time_obj = datetime.combine(datetime.today(), party_time)
    return time_obj.strftime('%I:%M %p') 

## admim (관리자 사용 API)
async def get_adminAccomodations(
    db: AsyncSession,
    isMostReviews: Optional[bool] = False,
    skip: int = 0,
    limit: int = 10
) -> List[dict]:
    if isMostReviews:
        query = (
            select(models.Accomodation)
            .outerjoin(models.Review)
            .group_by(models.Accomodation.id)
            .order_by(func.count(models.Review.id).desc())
        )
    else:
        query = (
            select(models.Accomodation)
            .order_by(asc(models.Accomodation.date))
        )
    
    result = await db.execute(query.offset(skip).limit(limit))
    accomodations = result.scalars().all()
    
    response = [
        {
            "id": accomodation.id,
            "name": accomodation.name,
            "address": accomodation.address,
            "number": accomodation.number,
            "date": format_date(accomodation.date)
        }
        for accomodation in accomodations
    ]
    
    return response

async def get_adminOwners(db: AsyncSession, isOldestOrders: Optional[bool] = False, skip: int = 0, limit: int = 10):
    query = select(models.Owner).offset(skip).limit(limit)
    query = query.order_by(models.Owner.date if isOldestOrders else desc(models.Owner.date))

    result = await db.execute(query)
    owners = result.scalars().all()

    response = [
        {
            "id": owner.id,
            "name": owner.name,
            "username": owner.username,
            "phoneNumber": owner.phoneNumber,
            "isAuth": owner.role == "ROLE_AUTH_OWNER"
        }
        for owner in owners
    ]
    return response

async def put_auth_adminOwners(db: AsyncSession, id: int):
    result = await db.execute(
        select(models.Owner).filter(models.Owner.id == id)
    )
    db_owner = result.scalar_one_or_none()
    if db_owner:
        db_owner.role = "ROLE_AUTH_OWNER"
        await db.commit()
        await db.refresh(db_owner)
        return {"msg": "ok"}  
    else:
        return {"msg": "fail"}

async def put_deny_adminOwners(db: AsyncSession, id: int):
    result = await db.execute(
        select(models.Owner).filter(models.Owner.id == id)
    )
    db_owner = result.scalar_one_or_none()
    if db_owner:
        db_owner.role = "ROLE_NOTAUTH_OWNER"
        await db.commit()
        await db.refresh(db_owner)
        return {"msg": "ok"}  
    else:
        return {"msg": "fail"}




## owner (사장님 사용 API)
async def get_ownerAccomodation(
    id: int,
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10
) -> List[dict]:
    query = (
            select(models.Accomodation)
            .filter(models.Accomodation.owner_id == id) 
            .order_by(asc(models.Accomodation.date))
        )

    result = await db.execute(query.offset(skip).limit(limit))
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
    return response

async def post_ownerAccomodation(db: AsyncSession, accomodation: schemas.OwnerAccomodationsPost):
    db_accomodation = models.Accomodation(
        owner_id=accomodation.id,
        name=accomodation.name,
        address=accomodation.address,
        introduction=accomodation.introduction,
        number=accomodation.number,
        date = format_dates(datetime.now())
    )
    db.add(db_accomodation)
    await db.commit()
    await db.refresh(db_accomodation)
    
    return {
        "id": db_accomodation.id, 
        "name": db_accomodation.name,
        "address": db_accomodation.address,
        "number": db_accomodation.number,
        "introduction": db_accomodation.introduction,
    }

async def put_ownerAccomodation(db: AsyncSession, id: int, accomodation: schemas.OwnerAccomodationsPut):
    result = await db.execute(
        select(models.Accomodation).filter(models.Accomodation.id == id)
    )
    db_accomodation = result.scalar_one_or_none()
    if db_accomodation:
        db_accomodation.name = accomodation.name
        db_accomodation.address = accomodation.address
        db_accomodation.number = accomodation.number
        db_accomodation.introduction = accomodation.introduction
        db_accomodation.date = format_dates(datetime.now())
        
        await db.commit()
        await db.refresh(db_accomodation)
        
        return {
            "id": db_accomodation.id, 
            "name": db_accomodation.name,
            "address": db_accomodation.address,
            "number": db_accomodation.number,
            "introduction": db_accomodation.introduction
        }
    else:
        return {"msg": "fail"}



async def get_ownermanagers(
    id: int,
    db: AsyncSession,
    isOldestOrders: Optional[bool] = False,
    skip: int = 0,
    limit: int = 10
) -> List[dict]:
    if isOldestOrders:
        query = (
                select(models.Manager)
                .filter(models.Manager.owner_id == id) 
                .order_by(desc(models.Manager.date))
            )
    else:
        query = (
                select(models.Manager)
                .filter(models.Manager.owner_id == id) 
                .order_by(asc(models.Manager.date))
            )

    result = await db.execute(query.offset(skip).limit(limit))
    managers = result.scalars().all()
    
    response = [
            {
                "id": manager.id,
                "name": manager.name,
                "username": manager.username,
                "phoneNumber": manager.phoneNumber,
                "date": format_date(manager.date),
                "isAuth": manager.role == "ROLE_AUTH_OWNER"
            }
            for manager in managers
        ]
    return response




## owner , manager(사장님 And 매니저 사용 API)
async def get_managerParties(
    id: int,
    db: AsyncSession,
    isOldestOrders: Optional[bool] = False,
    skip: int = 0,
    limit: int = 10
) -> List[dict]:
    if isOldestOrders:
        query = (
            select(models.Party)
            .outerjoin(models.Accomodation)
            .options(joinedload(models.Party.partys))
            .filter(models.Party.accomodation_id == id) 
            .order_by(func.count(models.Party.id).desc())
        )
    else:
        query = (
            select(models.Party)
            .outerjoin(models.Accomodation)
            .options(joinedload(models.Party.partys))
            .filter(models.Party.accomodation_id == id) 
            .order_by(func.count(models.Party.id).asc())
        )
    
    result = await db.execute(query.offset(skip).limit(limit))
    managerParties = result.scalars().all()
    
    response = [
        {
            "id": managerParty.id,
            "partyDate": format_date(managerParty.partyDate),
            "number": managerParty.number,
            "partyOpen": managerParty.partyOpen,
            "partyTime": format_party_time(managerParty.partyTime)
        }
        for managerParty in managerParties
    ]
    
    return response



