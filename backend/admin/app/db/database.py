from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from ..utils.utils import load_config
from sqlalchemy.ext.declarative import declarative_base

config = load_config("config.yaml")

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = f"mysql+aiomysql://{config['database']['user']}:{config['database']['password']}@{config['database']['host']}:{config['database']['port']}/{config['database']['name']}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=50,
    max_overflow=10,
    pool_recycle=3600
    )

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=AsyncSession
    )

async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
