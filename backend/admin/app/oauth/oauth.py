from ..db.crud import format_dates
from ..utils.utils import load_config
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt


config = load_config("config.yaml")

def create_access_token(data: dict):
    try:
        to_encode = data.copy()
        expire = format_dates(datetime.now() + timedelta(minutes=config['ACCESS_TOKEN_EXPIRE_MINUTES'])) 
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, config['SECRET_KEY'], algorithm=config['ALGORITHM'])
        return encoded_jwt
    except Exception as e:
        raise HTTPException(status_code=500, detail={"msg": "fail"})

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config['Token'])

def get_current_owner(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, config['SECRET_KEY'], algorithms=[config['ALGORITHM']])
        owner_id = payload.get("sub")
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