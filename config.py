# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./bagger.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60 * 24
    APP_TITLE: str = "Bagger API"
    APP_DESCRIPTION: str = "Bag that idea"
    APP_VERSION: str = "1.0.0"


# ← ADD THIS LINE (lowercase 'settings')
settings = Settings()