from ..utils.utils import load_config
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt


config = load_config("config.yaml")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=config['ACCESS_TOKEN_EXPIRE_MINUTES'])
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config['SECRET_KEY'], algorithm=config['ALGORITHM'])
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config['Token'])

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, config['SECRET_KEY'], algorithms=[config['ALGORITHM']])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    return user_id

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)