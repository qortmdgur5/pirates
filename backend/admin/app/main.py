from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .db import crud, database
from .utils import schemas

app = FastAPI()

# 등록한 업체 CRUD
@app.get("/companies", response_model=list[schemas.Company], summary="업체 리스트", tags=["company"])
async def read_companies(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
    companies = await crud.get_companies(db, skip=skip, limit=limit)
    return companies

@app.get("/companys/{id}", response_model=schemas.Company, summary="업체 조회", tags=["company"])
async def read_company(id: int, db: AsyncSession = Depends(database.get_db)):
    company = await crud.get_company(db, company_id=id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@app.post("/company", response_model=schemas.Company, summary="업체 등록", tags=["company"])
async def create_company(company: schemas.CompanyCreate, db: AsyncSession = Depends(database.get_db)):
    """
    업체 등록.

    - **name**: 업체명.
    - **is_active**: 업체 권한 (0:비활성화, 1:활성화).
    """
    return await crud.create_company(db=db, company=company)

@app.put("/company/{id}", response_model=schemas.Company, summary="업체 수정", tags=["company"])
async def update_company(id: int, company: schemas.CompanyUpdate, db: AsyncSession = Depends(database.get_db)):
    return await crud.update_company(db=db, company_id=id, company=company)

@app.delete("/company/{id}", response_model=schemas.Company, summary="업체 삭제", tags=["company"])
async def delete_company(id: int, db: AsyncSession = Depends(database.get_db)):
    return await crud.delete_company(db=db, company_id=id)

# 관리자 CRUD
@app.get("/admins", response_model=list[schemas.Admin], summary="관리자 리스트", tags=["admin"])
async def read_admins(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
    admins = await crud.get_admins(db, skip=skip, limit=limit)
    return admins

@app.get("/admin/{id}", response_model=schemas.Admin, summary="관리자 조회", tags=["admin"])
async def read_admin(id: int, db: AsyncSession = Depends(database.get_db)):
    admin = await crud.get_admin(db, admin_id=id)
    if admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin

@app.post("/admin", response_model=schemas.Admin, summary="관리자 등록", tags=["admin"])
async def create_admin(admin: schemas.AdminCreate, db: AsyncSession = Depends(database.get_db)):
    """
    관리자 등록.

    - **username**: 관리자명.
    - **password**: 관리자 패스워드.
    - **role**: 관리자 권한 (SUPER_ADMIN, ADMIN, VIEWER).
    """
    return await crud.create_admin(db=db, admin=admin)