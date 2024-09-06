from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import crud, database
from .utils import schemas

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.get("/companys", response_model=list[schemas.Company])
def read_companies(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    companies = crud.get_companies(db, skip=skip, limit=limit)
    return companies

@app.get("/companys/{id}", response_model=schemas.Company)
def read_company(id: int, db: Session = Depends(database.get_db)):
    company = crud.get_company(db, company_id=id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@app.post("/company/{id}", response_model=schemas.Company)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(database.get_db)):
    return crud.create_company(db=db, company=company)

@app.put("/company/{id}", response_model=schemas.Company)
def update_company(id: int, company: schemas.CompanyUpdate, db: Session = Depends(database.get_db)):
    return crud.update_company(db=db, company_id=id, company=company)

@app.delete("/company/{id}", response_model=schemas.Company)
def delete_company(id: int, db: Session = Depends(database.get_db)):
    return crud.delete_company(db=db, company_id=id)