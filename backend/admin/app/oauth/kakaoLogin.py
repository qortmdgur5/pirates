import requests
from ..utils.utils import load_config
from fastapi import HTTPException
from ..utils import schemas
from ..db import crud, database

config = load_config("config.yaml")

KAKAO_CLIENT_ID = config['KAKAO_CLIENT_ID']
KAKAO_REDIRECT_URI = config['KAKAO_REDIRECT_URI']

async def kakao_login_data(db):
    try:
        kakao_auth_url = (
                f"https://kauth.kakao.com/oauth/authorize"
                f"?client_id={KAKAO_CLIENT_ID}"
                f"&redirect_uri={KAKAO_REDIRECT_URI}"
                f"&response_type=code"
            )
        return kakao_auth_url
    
    except ValueError as e:
        error_message = str(e)
        print("ValueError:", error_message)
        await crud.log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": error_message})
    except Exception as e:
        error_message = str(e)
        print("Exception:", error_message)
        await crud.log_error(db, error_message)
        raise HTTPException(status_code=500, detail={"msg": error_message})
    
async def kakao_callback_data(db, code):
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
        return user_info
    
    except ValueError as e:
        error_message = str(e)
        print("ValueError:", error_message)
        await crud.log_error(db, error_message)
        raise HTTPException(status_code=400, detail={"msg": error_message})
    except Exception as e:
        error_message = str(e)
        print("Exception:", error_message)
        await crud.log_error(db, error_message)
        raise HTTPException(status_code=500, detail={"msg": error_message})
        