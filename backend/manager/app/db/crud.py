
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils import models, schemas
from ..service.manager import get_password_hash, verify_password
from fastapi import HTTPException


# 회원가입 처리 함수
async def create_user(db: AsyncSession, user: schemas.UserCreate):
    # 이메일 중복 체크
    result = await db.execute(select(models.User).filter(models.User.email == user.email))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 비밀번호 해싱 및 사용자 생성
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# 로그인 처리 함수
async def authenticate_user(db: AsyncSession, user: schemas.UserCreate):
    result = await db.execute(select(models.User).filter(models.User.email == user.email))
    db_user = result.scalars().first()

    if db_user is None or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return {"msg": "Login successful"}