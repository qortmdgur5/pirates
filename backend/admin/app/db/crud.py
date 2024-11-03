import os
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import func, select, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils import models
from ..utils import schemas
from ..service.admin import hash_password
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
import qrcode

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
    try:
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
                .order_by(asc(models.Accomodation.id))
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
    except ValueError as e:
        error_message = f"Date/Time parsing error: {str(e)}"
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": "fail"})
    
async def get_adminOwners(db: AsyncSession, isOldestOrders: Optional[bool] = False, skip: int = 0, limit: int = 10):
    try:
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
                "isAuth": True if owner.role == "ROLE_AUTH_OWNER" else False
            }
            for owner in owners
        ]
        return response
    except ValueError as e:
        error_message = f"Date/Time parsing error: {str(e)}"
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": "fail"})
    
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
        except ValueError as e:
            error_message = f"Date/Time parsing error: {str(e)}"
            await log_error(db, error_message)
            raise HTTPException(status_code=400, detail={"msg": "fail"})
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
        except ValueError as e:
            error_message = f"Date/Time parsing error: {str(e)}"
            await log_error(db, error_message)
            raise HTTPException(status_code=400, detail={"msg": "fail"})
    else:
        return {"msg": "fail"}




## owner (사장님 사용 API)
async def get_ownerAccomodation(
    id: int,
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10
) -> List[dict]:
    try:
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
    except ValueError as e:
        error_message = f"Date/Time parsing error: {str(e)}"
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": "fail"})

async def post_ownerAccomodation(db: AsyncSession, accomodation: schemas.OwnerAccomodationsPost):
    try:
        qr_directory = "/home/qr_directory"
        os.makedirs(qr_directory, exist_ok=True)
        
        base_url = "https://www.naver.com"
        qr_data = f"{base_url}"
        
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
    except ValueError as e:
        error_message = f"Date/Time parsing error: {str(e)}"
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": "fail"})

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
        except ValueError as e:
            error_message = f"Date/Time parsing error: {str(e)}"
            await log_error(db, error_message)
            raise HTTPException(status_code=400, detail={"msg": "fail"})
    else:
        return {"msg": "fail"}


async def get_ownermanagers(
    id: int,
    db: AsyncSession,
    isOldestOrders: Optional[bool] = False,
    skip: int = 0,
    limit: int = 10
) -> List[dict]:
    try:
        if isOldestOrders:
            query = (
                    select(models.Manager)
                    .filter(models.Manager.owner_id == id) 
                    .order_by(asc(models.Manager.id))
                )
        else:
            query = (
                    select(models.Manager)
                    .filter(models.Manager.owner_id == id) 
                    .order_by(desc(models.Manager.id))
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
                    "isAuth": True if manager.role == "ROLE_AUTH_MANAGER" else False 
                }
                for manager in managers
            ]
        return response
    except ValueError as e:
        error_message = f"Date/Time parsing error: {str(e)}"
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": "fail"})



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
        except ValueError as e:
            error_message = f"Date/Time parsing error: {str(e)}"
            await log_error(db, error_message)
            raise HTTPException(status_code=400, detail={"msg": "fail"})
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

        except ValueError as e:
            error_message = f"Date/Time parsing error: {str(e)}"
            await log_error(db, error_message)
            raise HTTPException(status_code=400, detail={"msg": "fail"})
    else:
        return {"msg": "fail"}


## owner , manager(사장님 And 매니저 사용 API)
async def get_managerParties(
    id: int,
    db: AsyncSession,
    isOldestOrders: Optional[bool] = False,
    skip: int = 0,
    limit: int = 10
) -> List[dict]:
    try:
        order_by_field = models.Party.partyDate.asc() if isOldestOrders else models.Party.partyDate.desc()

        query = (
            select(models.Party)
            .filter(models.Party.accomodation_id == id)
            .order_by(order_by_field)
            .offset(skip)
            .limit(limit)
        )
        
        result = await db.execute(query)
        managerParties = result.scalars().all()
        
        # Format the response
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
    
    except ValueError as e:
        error_message = f"Date/Time parsing error: {str(e)}"
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": "fail"})



async def post_managerParty(db: AsyncSession, party: schemas.managerParties):
    try:
        formatted_date = datetime.strptime(party.partyDate, "%Y-%m-%d").strftime("%Y.%m.%d")
        formatted_time = datetime.strptime(party.partyTime, "%H-%M-%S").strftime("%H:%M:%S")
        
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
    
    except ValueError as e:
        error_message = f"Date/Time parsing error: {str(e)}"
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": "fail"})

async def put_managerParty(db: AsyncSession, id: int, party: schemas.managerParties):
    result = await db.execute(
        select(models.Party).filter(models.Party.id == id)
    )
    
    db_party = result.scalar_one_or_none()
    if db_party:
        try:
            formatted_date = datetime.strptime(party.partyDate, "%Y-%m-%d").strftime("%Y.%m.%d")
            formatted_time = datetime.strptime(party.partyTime, "%H-%M-%S").strftime("%H:%M:%S")
            db_party.partyDate = formatted_date
            db_party.number = party.number
            db_party.partyOpen = party.partyOpen
            db_party.partyTime = formatted_time
            await db.commit()
            await db.refresh(db_party)
            return {"msg": "ok"}  
        
        except ValueError as e:
            error_message = f"Date/Time parsing error: {str(e)}"
            await log_error(db, error_message)
            raise HTTPException(status_code=400, detail={"msg": "fail"})
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
        
        except ValueError as e:
            error_message = f"Date/Time parsing error: {str(e)}"
            await log_error(db, error_message)
            raise HTTPException(status_code=400, detail={"msg": "fail"})
    else:
        return {"msg": "fail"}
    
    
async def get_managerParty(
    id: int,
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10
) -> List[dict]:
    try:
        query = (
            select(models.Participant, models.Party)
            .outerjoin(models.Party, models.Participant.party_id == models.Party.id)
            .filter(models.Participant.party_id == id)
            .offset(skip)
            .limit(limit)
        )
        
        result = await db.execute(query)
        managerParties = result.fetchall()

        print("managerParties : ", managerParties)
        response = [
            {
                "id": participant.id,
                "partyDate": format_date(party.partyDate) if party.partyDate else None,
                "number": party.number if party else 0,
                "partyTime": format_party_time(party.partyTime) if party.partyTime else None,
                "name": participant.name,
                "phone": participant.phone,
                "age": participant.age,
                "gender": "남자" if participant.gender else "여자" 
            }
            for participant, party in managerParties
        ]
        
        return response
    
    except ValueError as e:
        error_message = f"Date/Time parsing error: {str(e)}"
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": "fail"})
    
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
    
    except ValueError as e:
        error_message = f"Date/Time parsing error: {str(e)}"
        await log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": "fail"})


    
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
        
        except ValueError as e:
            error_message = f"Date/Time parsing error: {str(e)}"
            await log_error(db, error_message)
            raise HTTPException(status_code=400, detail={"msg": "fail"})
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
        
        except ValueError as e:
            error_message = f"Date/Time parsing error: {str(e)}"
            await log_error(db, error_message)
            raise HTTPException(status_code=400, detail={"msg": "fail"})
    else:
        return {"msg": "fail"}
    
async def get_managerAccomodationQR(
    id: int,
    db: AsyncSession
) -> List[dict]:
    try:
        query = (
                select(models.Accomodation)
                .filter(models.Accomodation.id == id) 
            )

        result = await db.execute(query)
        accomodation = result.scalar_one_or_none()
        
        if not accomodation:
            raise HTTPException(status_code=404, detail={"msg": "Accommodation not found"})
        
        qr_code_path = accomodation.directory
        if not qr_code_path or not os.path.exists(qr_code_path):
            raise HTTPException(status_code=404, detail={"msg": "QR code file not found"})
        
        return qr_code_path  
    except Exception  as e:
        await log_error(db, str(e))
        raise HTTPException(status_code=400, detail={"msg": "fail"})