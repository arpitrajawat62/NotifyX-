import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    SMTP_EMAIL= os.getenv("SMPTP_EMAIL")
    SMTP_PASSWORD= os.getenv("SMTP PASSWORD")
    SECRET_KEY= os.getenv("SECRET_KEY")
    ALGORITHM= os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES= os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    RAPIDAPI_KEY= os.getenv("RAPIDAPI_KEY")



Settings = Settings()