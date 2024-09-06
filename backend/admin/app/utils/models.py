from sqlalchemy import Column, Integer, String, Boolean
from ..db.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    is_active = Column(Boolean, default=True)
