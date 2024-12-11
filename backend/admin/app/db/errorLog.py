from sqlalchemy.ext.asyncio import AsyncSession
from ..utils import models
from ..utils.utils import load_config
from datetime import datetime, timedelta, timezone
import logging

config = load_config("config.yaml")

logging.basicConfig(
    level=logging.ERROR, 
    format="%(asctime)s - %(levelname)s - %(message)s",
     handlers=[
        logging.FileHandler("app_errors.log"),  
        logging.StreamHandler()  
    ])
logger = logging.getLogger("uvicorn.access")

async def log_error(db: AsyncSession, message: str):
    try:
        logging.error(f"Error: {message}") 
        error_log = models.ErrorLog(message=message)
        db.add(error_log)
        await db.commit()
    except Exception as log_error:
        print(f"Error while logging: {log_error}")
        logging.error(f"Error while logging to DB: {log_error}")
        
        
def format_date(date_obj):
    kst_date = date_obj + timedelta(hours=9)
    return kst_date.strftime("%y.%m.%d")

def format_dates(date_obj):
    kst_tz = timezone(timedelta(hours=9))
    return date_obj.astimezone(kst_tz)

def format_party_time(party_time: str) -> str:
    time_obj = datetime.combine(datetime.today(), party_time)
    return time_obj.strftime('%I:%M %p') 
