import os
from dotenv import load_dotenv
from ..db.errorLog import format_dates
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
TOKEN = os.getenv("TOKEN")

def create_access_token(data: dict):
    try:
        to_encode = data.copy()
        expire = format_dates(datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) 
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        raise HTTPException(status_code=500, detail={"msg": "fail"})

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN)

def get_current_owner(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
        owner_id = payload.get("owner_id")
        role = payload.get("role")
        accomodation_id = payload.get("accomodation_id")
        
        if owner_id is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.JWTError:
        raise credentials_exception

    return {"owner_id": owner_id, "role": role, "accomodation_id": accomodation_id}

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)