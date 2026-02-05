# routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from utils.auth import create_access_token, get_current_user

from models.user import User
from models.platform import Platform
from models.topic import Topic
from models.cheat import Cheat, CheatPlatform, CheatTopic
from models.user_cheat import UserCheat

from schemas.auth import UserCreate, UserResponse, UserLogin, TokenResponse
from schemas.taxonomy import PlatformResponse, TopicResponse
from schemas.cheat import CheatResponse, UserCheatResponse
from schemas.bootstrap import (
    BootstrapResponse,
    CheatPlatformLink,
    CheatTopicLink,
)

router = APIRouter()


def cheat_to_response(cheat: Cheat) -> CheatResponse:
    return CheatResponse(
        id=cheat.id,
        title=cheat.title,
        code=cheat.code,
        notes=cheat.notes,
        is_public=cheat.is_public,
        platform_ids=[p.platform_id for p in cheat.platforms],
        topic_ids=[t.topic_id for t in cheat.topics],
    )


@router.post("/", response_model=UserResponse)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists with this email",
        )

    new_user = User(email=user_in.email, name=user_in.name)
    new_user.set_password(user_in.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not user.check_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(user_id=user.id, is_admin=user.is_admin)
    return {"access_token": access_token, "token_type": "bearer", "user": user}


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/bootstrap", response_model=BootstrapResponse)
def bootstrap(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Reference data (global)
    platforms = db.query(Platform).order_by(Platform.name.asc()).all()
    topics = db.query(Topic).order_by(Topic.name.asc()).all()

    # Visible cheats: public + mine
    cheats = (
        db.query(Cheat)
        .filter((Cheat.is_public == True) | (Cheat.created_by_user_id == current_user.id))
        .all()
    )

    # Link tables
    cheat_platforms = db.query(CheatPlatform).all()
    cheat_topics = db.query(CheatTopic).all()

    # User overlay (favorites / personal notes)
    overlays = db.query(UserCheat).filter(UserCheat.user_id == current_user.id).all()

    # IMPORTANT: convert SQLAlchemy models -> Pydantic models (fixes Pylance + typing)
    return BootstrapResponse(
        user=UserResponse.model_validate(current_user),
        platforms=[PlatformResponse.model_validate(p) for p in platforms],
        topics=[TopicResponse.model_validate(t) for t in topics],
        cheats=[cheat_to_response(c) for c in cheats],
        cheat_platforms=[CheatPlatformLink(cheat_id=x.cheat_id, platform_id=x.platform_id) for x in cheat_platforms],
        cheat_topics=[CheatTopicLink(cheat_id=x.cheat_id, topic_id=x.topic_id) for x in cheat_topics],
        user_cheats=[UserCheatResponse.model_validate(x) for x in overlays],
    )
