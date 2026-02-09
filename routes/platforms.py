from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from database import get_db
from models.platform import Platform
from models.cheat import CheatPlatform
from schemas.taxonomy import TaxonomyCreate, PlatformUpdate

router = APIRouter()

def slugify(name: str) -> str:
    return name.strip().lower().replace(" ", "-")

@router.post("/", status_code=201)
def add_platform(data: TaxonomyCreate, db: Session = Depends(get_db)):
    slug = data.slug or slugify(data.name)
    platform = Platform(name=data.name, slug=slug, type=data.type or "language")
    db.add(platform)
    db.commit()
    return {"message": f"Added platform: {data.name}"}

@router.patch("/{platform_id}", status_code=200)
def update_platform(platform_id: int, patch: PlatformUpdate, db: Session = Depends(get_db)):
    platform = db.query(Platform).filter(Platform.id == platform_id).first()
    if not platform:
        raise HTTPException(404, "Platform not found")

    if patch.name is not None:
        platform.name = patch.name
    if patch.slug is not None:
        platform.slug = patch.slug
    if patch.type is not None:
        platform.type = patch.type

    db.commit()
    return {"message": "Platform updated"}

@router.delete("/{platform_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_platform(platform_id: int, db: Session = Depends(get_db)):
    platform = db.query(Platform).filter(Platform.id == platform_id).first()
    if not platform:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    in_use = db.query(CheatPlatform).filter(CheatPlatform.platform_id == platform_id).first()
    if in_use:
        raise HTTPException(409, "Platform is in use by cheats (remove links first)")

    db.delete(platform)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
