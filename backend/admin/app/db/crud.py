from sqlalchemy.orm import Session
from ..utils import models
from ..utils import schemas
from ..service.admin import hash_password

def get_companies(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Company).offset(skip).limit(limit).all()

def get_company(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()

def create_company(db: Session, company: schemas.CompanyCreate):
    db_company = models.Company(
        name=company.name,
        is_active=company.is_active
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def update_company(db: Session, company_id: int, company: schemas.CompanyUpdate):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if db_company:
        for key, value in company.dict().items():
            setattr(db_company, key, value)
        db.commit()
        db.refresh(db_company)
    return db_company

def delete_company(db: Session, company_id: int):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if db_company:
        db.delete(db_company)
        db.commit()
    return db_company


def get_admins(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Admin).offset(skip).limit(limit).all()

def get_admin(db: Session, admin_id: int):
    return db.query(models.Admin).filter(models.Company.id == admin_id).first()

def create_admin(db: Session, admin: schemas.AdminCreate):

    hashed_password = hash_password(admin.password)
    
    db_admin = models.Admin(
        username=admin.username,
        password=hashed_password, 
        role=admin.role
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin