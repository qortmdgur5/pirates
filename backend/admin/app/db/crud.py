
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils import models
from ..utils import schemas
from ..service.admin import hash_password

# 회사 CRUD
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




# 관리자 CRUD
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




# 사장 CRUD   
async def get_owners(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.Owner).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def get_owner(db: AsyncSession, owner_id: int):
    result = await db.execute(
        select(models.Owner).filter(models.Owner.id == owner_id)
    )
    return result.scalar_one_or_none()

async def create_owner(db: AsyncSession, owner: schemas.OwnerCreate):
    hashed_password = hash_password(owner.password)
    
    db_owner = models.Owner(
        username=owner.username,
        password=hashed_password,
    )
    db.add(db_owner)
    await db.commit()
    await db.refresh(db_owner)
    
    db_owner.date = db_owner.date.date()
    
    return db_owner

async def update_owner(db: AsyncSession, owner_id: int, owner: schemas.OwnerUpdate):
    result = await db.execute(
        select(models.Owner).filter(models.Owner.id == owner_id)
    )
    db_owner = result.scalar_one_or_none()
    if db_owner:
        for key, value in owner.dict().items():
            setattr(db_owner, key, value)
        await db.commit()
        await db.refresh(db_owner)
    return db_owner

async def delete_owner(db: AsyncSession, owner_id: int):
    result = await db.execute(
        select(models.Owner).filter(models.Owner.id == owner_id)
    )
    db_owner = result.scalar_one_or_none()
    if db_owner:
        await db.delete(db_owner)
        await db.commit()
    return db_owner



# 사장 권한 U
async def update_owner_role(db: AsyncSession, owner_id: int, owner: schemas.OwnerRole):
    result = await db.execute(
        select(models.Owner).filter(models.Owner.id == owner_id)
    )
    db_owner = result.scalar_one_or_none()
    if db_owner:
        for key, value in owner.dict().items():
            setattr(db_owner, key, value)
        await db.commit()
        await db.refresh(db_owner)
    return db_owner




# 숙소 CRUD
async def get_accommodations(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.Accommodation).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def get_accommodation(db: AsyncSession, accommodation_id: int):
    result = await db.execute(
        select(models.Accommodation).filter(models.Accommodation.id == accommodation_id)
    )
    return result.scalar_one_or_none()

async def create_accommodation(db: AsyncSession, accommodation: schemas.AccommodationCreate):
    db_accommodation = models.Accommodation(
        owner_id=accommodation.owner_id,
        name=accommodation.name,
        address=accommodation.address,
        introduction=accommodation.introduction
    )
    db.add(db_accommodation)
    await db.commit()
    await db.refresh(db_accommodation)
    
    db_accommodation.date = db_accommodation.date.date()
    
    return db_accommodation

async def update_accommodation(db: AsyncSession, accommodation_id: int, accommodation: schemas.AccommodationUpdate):
    result = await db.execute(
        select(models.Accommodation).filter(models.Accommodation.id == accommodation_id)
    )
    db_accommodation = result.scalar_one_or_none()
    if db_accommodation:
        for key, value in accommodation.dict().items():
            setattr(db_accommodation, key, value)
        await db.commit()
        await db.refresh(db_accommodation)
    return db_accommodation

async def delete_accommodation(db: AsyncSession, accommodation_id: int):
    result = await db.execute(
        select(models.Accommodation).filter(models.Accommodation.id == accommodation_id)
    )
    db_accommodation = result.scalar_one_or_none()
    if db_accommodation:
        await db.delete(db_accommodation)
        await db.commit()
    return db_accommodation
