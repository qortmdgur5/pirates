import os
from dotenv import load_dotenv
import requests
from fastapi import HTTPException
from ..db import errorLog
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

load_dotenv()
KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
KAKAO_REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")

async def kakao_login_data(id: Optional[str], db: AsyncSession):
    try:
        kakao_auth_url = (
            f"https://kauth.kakao.com/oauth/authorize"
            f"?client_id={KAKAO_CLIENT_ID}"
            f"&redirect_uri={KAKAO_REDIRECT_URI}"
            f"&response_type=code"
            f"&state={id}"
        )
        return kakao_auth_url
    
    except ValueError as e:
        error_message = str(e)
        print("ValueError:", error_message)
        await errorLog.log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": error_message})
    except Exception as e:
        error_message = str(e)
        print("Exception:", error_message)
        await errorLog.log_error(db, error_message)
        raise HTTPException(status_code=500, detail={"msg": error_message})
    
async def kakao_callback_data(db: AsyncSession, code: str, id: Optional[str]):
    try:
        token_url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": KAKAO_CLIENT_ID,
            "redirect_uri": KAKAO_REDIRECT_URI,
            "code": code,
        }
        token_response = requests.post(token_url, data=data)
        
        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get access token")
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        user_info_url = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        user_response = requests.get(user_info_url, headers=headers)

        if user_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get user info")
        user_info = user_response.json()
        return {"user_info": user_info, "id": id}
    
    except ValueError as e:
        error_message = str(e)
        print("ValueError:", error_message)
        await errorLog.log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": error_message})
    except Exception as e:
        error_message = str(e)
        print("Exception:", error_message)
        await errorLog.log_error(db, error_message)
        raise HTTPException(status_code=500, detail={"msg": error_message})
        