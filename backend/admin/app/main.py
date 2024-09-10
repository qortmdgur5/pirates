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




# 사장 CRUD
@app.get("/owners", response_model=list[schemas.Owner], summary="사장 리스트", tags=["owner"])
async def read_owners(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
    owners = await crud.get_owners(db, skip=skip, limit=limit)
    return owners

@app.get("/owner/{id}", response_model=schemas.Owner, summary="사장 조회", tags=["owner"])
async def read_owner(id: int, db: AsyncSession = Depends(database.get_db)):
    owner = await crud.get_owner(db, owner_id=id)
    if owner is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return owner

@app.post("/owner", response_model=schemas.Owner, summary="사장 등록", tags=["owner"])
async def create_owner(owner: schemas.OwnerCreate, db: AsyncSession = Depends(database.get_db)):
    """
    사장 등록.

    - **username**: 사장 아이디.
    - **password**: 사장 패스워드.
    """
    return await crud.create_owner(db=db, owner=owner)

@app.put("/owner/{id}", response_model=schemas.Owner, summary="사장 수정", tags=["owner"])
async def update_owner(id: int, owner: schemas.OwnerUpdate, db: AsyncSession = Depends(database.get_db)):
    return await crud.update_owner(db=db, owner_id=id, owner=owner)

@app.delete("/owner/{id}", response_model=schemas.Owner, summary="사장 삭제", tags=["owner"])
async def delete_owner(id: int, db: AsyncSession = Depends(database.get_db)):
    return await crud.delete_owner(db=db, owner_id=id)




# 사장 권한 U
@app.put("/owner/role/{id}", response_model=schemas.Owner, summary="사장 권한 수정", tags=["owner role"])
async def update_owner_role(id: int, owner: schemas.OwnerRole, db: AsyncSession = Depends(database.get_db)):
    """
    사장 권한 수정.

    - **role**: 승인 ROLE_AUTH_OWNER, 미승인 ROLE_NOTAUTH_OWNER.
    """
    return await crud.update_owner_role(db=db, owner_id=id, owner=owner)




# 숙소 CRUD
@app.get("/accommodations", response_model=list[schemas.Accommodation], summary="숙소 리스트", tags=["accommodation"])
async def read_accommodations(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
    accommodations = await crud.get_accommodations(db, skip=skip, limit=limit)
    return accommodations

@app.get("/accommodations/{id}", response_model=schemas.Accommodation, summary="숙소 조회", tags=["accommodation"])
async def read_accommodation(id: int, db: AsyncSession = Depends(database.get_db)):
    accommodation = await crud.get_accommodation(db, accommodation_id=id)
    if accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    return accommodation

@app.post("/accommodation", response_model=schemas.Accommodation, summary="숙소 등록", tags=["accommodation"])
async def create_accommodation(accommodation: schemas.AccommodationCreate, db: AsyncSession = Depends(database.get_db)):
    """
    숙소 등록.

    - **owner_id**: 사장 테이블 pk.
    - **name**: 게스트 하우스 이름.
    - **address**: 주소.
    - **introduction**: 숙소 소개말.
    """
    return await crud.create_accommodation(db=db, accommodation=accommodation)

@app.put("/accommodation/{id}", response_model=schemas.Accommodation, summary="숙소 수정", tags=["accommodation"])
async def update_accommodation(id: int, accommodation: schemas.AccommodationUpdate, db: AsyncSession = Depends(database.get_db)):
    return await crud.update_accommodation(db=db, accommodation_id=id, accommodation=accommodation)

@app.delete("/accommodation/{id}", response_model=schemas.Accommodation, summary="숙소 삭제", tags=["accommodation"])
async def delete_accommodation(id: int, db: AsyncSession = Depends(database.get_db)):
    return await crud.delete_accommodation(db=db, accommodation_id=id)



