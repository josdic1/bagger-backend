import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ENV: str = os.getenv("ENV", "development")

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./bagger.db")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_MINUTES: int = int(os.getenv("JWT_EXPIRATION_MINUTES", str(60 * 24)))

    APP_TITLE: str = os.getenv("APP_TITLE", "Bagger API")
    APP_DESCRIPTION: str = os.getenv("APP_DESCRIPTION", "Boutique Cheat Sheet System")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")

settings = Settings()
