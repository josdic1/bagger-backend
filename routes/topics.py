from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from database import get_db
from models.topic import Topic
from models.cheat import CheatTopic
from schemas.taxonomy import TaxonomyCreate, TopicUpdate

router = APIRouter()

def slugify(name: str) -> str:
    return name.strip().lower().replace(" ", "-")

@router.post("/", status_code=201)
def add_topic(data: TaxonomyCreate, db: Session = Depends(get_db)):
    slug = data.slug or slugify(data.name)
    topic = Topic(name=data.name, slug=slug)
    db.add(topic)
    db.commit()
    return {"message": f"Added topic: {data.name}"}

@router.patch("/{topic_id}", status_code=200)
def update_topic(topic_id: int, patch: TopicUpdate, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(404, "Topic not found")

    if patch.name is not None:
        topic.name = patch.name
    if patch.slug is not None:
        topic.slug = patch.slug

    db.commit()
    return {"message": "Topic updated"}

@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    in_use = db.query(CheatTopic).filter(CheatTopic.topic_id == topic_id).first()
    if in_use:
        raise HTTPException(409, "Topic is in use by cheats (remove links first)")

    db.delete(topic)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
