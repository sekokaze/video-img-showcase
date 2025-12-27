import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "***")
    FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "***")
    BASE_ID = os.getenv("BASE_ID", "***")
    TABLE_ID = os.getenv("TABLE_ID", "***")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
