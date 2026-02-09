from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from database import get_db
from utils.auth import get_current_user

from models.user import User
from models.cheat import Cheat, CheatPlatform, CheatTopic
from models.platform import Platform
from models.topic import Topic
from models.user_cheat import UserCheat

from schemas.cheat import (
    CheatCreate,
    CheatUpdate,
    CheatResponse,
    UserCheatUpdate,
    UserCheatResponse,
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


# =========================
# CHEATS
# =========================

@router.get("/", response_model=list[CheatResponse])
def list_visible_cheats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cheats = (
        db.query(Cheat)
        .filter((Cheat.is_public == True) | (Cheat.created_by_user_id == current_user.id))
        .all()
    )
    return [cheat_to_response(c) for c in cheats]


@router.post("/", response_model=CheatResponse, status_code=status.HTTP_201_CREATED)
def create_cheat(
    cheat_in: CheatCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Validate ids exist
    if cheat_in.platform_ids:
        found = db.query(Platform).filter(Platform.id.in_(cheat_in.platform_ids)).count()
        if found != len(set(cheat_in.platform_ids)):
            raise HTTPException(400, "One or more platform_ids are invalid")

    if cheat_in.topic_ids:
        found = db.query(Topic).filter(Topic.id.in_(cheat_in.topic_ids)).count()
        if found != len(set(cheat_in.topic_ids)):
            raise HTTPException(400, "One or more topic_ids are invalid")

    cheat = Cheat(
        title=cheat_in.title,
        code=cheat_in.code,
        notes=cheat_in.notes,
        created_by_user_id=current_user.id,
        is_public=cheat_in.is_public,
    )
    db.add(cheat)
    db.flush()  # get cheat.id

    for pid in set(cheat_in.platform_ids):
        db.add(CheatPlatform(cheat_id=cheat.id, platform_id=pid))

    for tid in set(cheat_in.topic_ids):
        db.add(CheatTopic(cheat_id=cheat.id, topic_id=tid))

    db.commit()
    db.refresh(cheat)
    return cheat_to_response(cheat)


@router.patch("/{cheat_id}", response_model=CheatResponse)
def update_cheat(
    cheat_id: int,
    patch: CheatUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cheat = db.query(Cheat).filter(Cheat.id == cheat_id).first()
    if not cheat:
        raise HTTPException(404, "Cheat not found")

    if cheat.created_by_user_id != current_user.id:
        raise HTTPException(403, "Not allowed")

    if patch.title is not None:
        cheat.title = patch.title
    if patch.code is not None:
        cheat.code = patch.code
    if patch.notes is not None:
        cheat.notes = patch.notes
    if patch.is_public is not None:
        cheat.is_public = patch.is_public

    # Replace join rows if arrays provided
    if patch.platform_ids is not None:
        # validate
        if patch.platform_ids:
            found = db.query(Platform).filter(Platform.id.in_(patch.platform_ids)).count()
            if found != len(set(patch.platform_ids)):
                raise HTTPException(400, "One or more platform_ids are invalid")

        db.query(CheatPlatform).filter(CheatPlatform.cheat_id == cheat.id).delete()
        for pid in set(patch.platform_ids):
            db.add(CheatPlatform(cheat_id=cheat.id, platform_id=pid))

    if patch.topic_ids is not None:
        # validate
        if patch.topic_ids:
            found = db.query(Topic).filter(Topic.id.in_(patch.topic_ids)).count()
            if found != len(set(patch.topic_ids)):
                raise HTTPException(400, "One or more topic_ids are invalid")

        db.query(CheatTopic).filter(CheatTopic.cheat_id == cheat.id).delete()
        for tid in set(patch.topic_ids):
            db.add(CheatTopic(cheat_id=cheat.id, topic_id=tid))

    db.commit()
    db.refresh(cheat)
    return cheat_to_response(cheat)


@router.delete("/{cheat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cheat(
    cheat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cheat = db.query(Cheat).filter(Cheat.id == cheat_id).first()
    if not cheat:
        raise HTTPException(404, "Cheat not found")

    if cheat.created_by_user_id != current_user.id:
        raise HTTPException(403, "Not allowed")

    # Remove overlays first (safe)
    db.query(UserCheat).filter(UserCheat.cheat_id == cheat.id).delete()

    # Remove join rows
    db.query(CheatPlatform).filter(CheatPlatform.cheat_id == cheat.id).delete()
    db.query(CheatTopic).filter(CheatTopic.cheat_id == cheat.id).delete()

    db.delete(cheat)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# =========================
# USER OVERLAY (me)
# =========================

@router.patch("/{cheat_id}/me", response_model=UserCheatResponse)
def update_my_overlay(
    cheat_id: int,
    patch: UserCheatUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cheat = db.query(Cheat).filter(Cheat.id == cheat_id).first()
    if not cheat:
        raise HTTPException(404, "Cheat not found")

    overlay = db.query(UserCheat).filter(
        UserCheat.user_id == current_user.id,
        UserCheat.cheat_id == cheat_id,
    ).first()

    if not overlay:
        overlay = UserCheat(user_id=current_user.id, cheat_id=cheat_id)
        db.add(overlay)

    if patch.is_favorite is not None:
        overlay.is_favorite = patch.is_favorite
    if patch.personal_notes is not None:
        overlay.personal_notes = patch.personal_notes

    db.commit()
    db.refresh(overlay)
    return overlay


@router.delete("/{cheat_id}/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_overlay(
    cheat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    overlay = db.query(UserCheat).filter(
        UserCheat.user_id == current_user.id,
        UserCheat.cheat_id == cheat_id,
    ).first()

    if not overlay:
        # deleting something that doesn't exist is fine
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    db.delete(overlay)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)