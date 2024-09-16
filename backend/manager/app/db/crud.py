
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils import models, schemas
from ..service.password import get_password_hash, verify_password
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

# 파티방 관리
## 파티방 등록
async def create_party(db: AsyncSession, party: schemas.PartyBase):
    db_party = models.Party(
        accommodation_id=party.accommodation_id,
        partyDate=party.partyDate,
        partyOpen=party.partyOpen,
        partyTime=party.partyTime,
        number=party.number,
        partyOn=party.partyOn
    )
    db.add(db_party)
    await db.commit()
    await db.refresh(db_party)
    return db_party

## 날짜별 파티방 리스트
async def party_list(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.Party).offset(skip).limit(limit)
    )
    return result.scalars().all()

## 전체 명단 리스트
async def party_participant(db: AsyncSession, party_id: int, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.Participant).filter(models.Participant.party_id == party_id).offset(skip).limit(limit)
    )
    return result.scalars().all()

## 파티방 명단 생성
async def create_party_participant(db: AsyncSession, participant: schemas.Participant):
    
    db_participant = models.Participant(
        party_id=participant.party_id,
        name=participant.name,
        phone=participant.phone,
        mbti=participant.mbti,
        age=participant.age,
        region=participant.region,
        gender=participant.gender
    )
    db.add(db_participant)
    await db.commit()
    await db.refresh(db_participant)
    
    return db_participant

## 파티방 명단 수정
async def update_party_participant(db: AsyncSession, participant_id: int, participant: schemas.Participant):
    result = await db.execute(
        select(models.Participant).filter(models.Participant.id == participant_id)
    )
    db_participant = result.scalar_one_or_none()
    if db_participant:
        for key, value in participant.dict().items():
            setattr(db_participant, key, value)
        await db.commit()
        await db.refresh(db_participant)
    return db_participant

## 파티방 명단 삭제
async def delete_party_participant(db: AsyncSession, participant_id: int):
    result = await db.execute(
        select(models.Participant).filter(models.Participant.id == participant_id)
    )
    db_participant = result.scalar_one_or_none()
    if db_participant:
        await db.delete(db_participant)
        await db.commit()
    return db_participant