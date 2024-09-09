
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils import models
from ..utils import schemas
from ..service.admin import hash_password

async def get_companies(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.Company).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def get_company(db: AsyncSession, company_id: int):
    result = await db.execute(
        select(models.Company).filter(models.Company.id == company_id)
    )
    return result.scalar_one_or_none()

async def create_company(db: AsyncSession, company: schemas.CompanyCreate):
    db_company = models.Company(
        name=company.name,
        is_active=company.is_active
    )
    db.add(db_company)
    await db.commit()
    await db.refresh(db_company)
    return db_company

async def update_company(db: AsyncSession, company_id: int, company: schemas.CompanyUpdate):
    result = await db.execute(
        select(models.Company).filter(models.Company.id == company_id)
    )
    db_company = result.scalar_one_or_none()
    if db_company:
        for key, value in company.dict().items():
            setattr(db_company, key, value)
        await db.commit()
        await db.refresh(db_company)
    return db_company

async def delete_company(db: AsyncSession, company_id: int):
    result = await db.execute(
        select(models.Company).filter(models.Company.id == company_id)
    )
    db_company = result.scalar_one_or_none()
    if db_company:
        await db.delete(db_company)
        await db.commit()
    return db_company

async def get_admins(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.Admin).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def get_admin(db: AsyncSession, admin_id: int):
    result = await db.execute(
        select(models.Admin).filter(models.Admin.id == admin_id)
    )
    return result.scalar_one_or_none()

async def create_admin(db: AsyncSession, admin: schemas.AdminCreate):
    hashed_password = hash_password(admin.password)
    
    db_admin = models.Admin(
        username=admin.username,
        password=hashed_password, 
        role=admin.role
    )
    db.add(db_admin)
    await db.commit()
    await db.refresh(db_admin)
    return db_admin
