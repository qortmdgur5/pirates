import os
from dotenv import load_dotenv
from sqlalchemy import func, select, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from .errorLog import format_date, log_error, format_dates
from ..utils import models, schemas
from typing import List, Optional
from datetime import datetime
from ..oauth.password import hash_password, verify_password
import qrcode
from urllib.parse import urlencode

load_dotenv()
QR_DIRECTORY = os.getenv("QR_DIRECTORY")
QR_CODE = os.getenv("QR_CODE")

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
        db_accomodation = models.Accomodation(
            owner_id=accomodation.id,
            name=accomodation.name,
            address=accomodation.address,
            introduction=accomodation.introduction,
            number=accomodation.number,
            date=format_dates(datetime.now()),
        )
        db.add(db_accomodation)
        await db.commit()  
        await db.refresh(db_accomodation)
        accomodation_id = db_accomodation.id 

        qr_directory = QR_DIRECTORY
        os.makedirs(qr_directory, exist_ok=True) 
        
        base_url = QR_CODE
        query_params = {
            "id": accomodation_id 
        }
        full_url = f"{base_url}?{urlencode(query_params)}"
        
        qr_img = qrcode.make(full_url)
        qr_filename = f"{accomodation_id}_{accomodation.name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        qr_path = os.path.join(qr_directory, qr_filename)
        qr_img.save(qr_path)  
        
        query = select(models.Accomodation).filter(models.Accomodation.id == accomodation_id)
        result = await db.execute(query)
        accomodation_to_update = result.scalar_one_or_none()  
        if accomodation_to_update:
            accomodation_to_update.directory = qr_path 
            await db.commit()  
            await db.refresh(accomodation_to_update) 
        
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
    pageSize: int = 10,
    name: Optional[str] = None
) -> List[dict]:
    try:
        offset = max(page * pageSize, 0)

        query = select(models.Manager).filter(models.Manager.owner_id == id)
        
        if name:
            query = query.filter(models.Manager.name.ilike(f"%{name}%"))

        query = query.order_by(asc(models.Manager.id) if isOldestOrders else desc(models.Manager.id))
        query = query.offset(offset).limit(pageSize)
        
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
