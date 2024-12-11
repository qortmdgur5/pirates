from sqlalchemy import func, select, desc, asc, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from .errorLog import format_date, log_error
from ..utils import models
from typing import List, Optional

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