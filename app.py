from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import engine, Base, SessionLocal
from config import settings
from routes.users import router as user_router
from routes.cheats import router as cheat_router
from seed import seed_if_empty


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables (until Alembic)
    Base.metadata.create_all(bind=engine)

    # Seed taxonomy if empty
    db = SessionLocal()
    try:
        seed_if_empty(db)
    finally:
        db.close()

    yield


app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api/users", tags=["Users"])
app.include_router(cheat_router, prefix="/api/cheats", tags=["Cheats"])


@app.get("/")
def home():
    return {"message": f"{settings.APP_TITLE} is online."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
