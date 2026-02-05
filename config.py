import os
from dotenv import load_dotenv

# Load the .env file from your root directory
load_dotenv()

class Settings:
    # Prioritizes the DATABASE_URL in your .env (catering.db)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./bagger.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60 * 24
    APP_TITLE: str = "Bagger API"
    APP_DESCRIPTION: str = "Boutique Cheat Sheet System"
    APP_VERSION: str = "1.0.0"



# Instantiate so we can import 'settings' elsewhere
settings = Settings()