from sqlalchemy.orm import Session
from models.platform import Platform
from models.topic import Topic


DEFAULT_PLATFORMS = [
    ("CSS", "css", "language"),
    ("HTML", "html", "language"),
    ("JavaScript", "javascript", "language"),
    ("Python", "python", "language"),
    ("React", "react", "framework"),
    ("SQL", "sql", "language"),
    ("Terminal", "terminal", "tool"),
    ("Regex", "regex", "tool"),
    ("JSON", "json", "format"),
    ("XML", "xml", "format"),
]

DEFAULT_TOPICS = [
    ("Arrays", "arrays"),
    ("Classes", "classes"),
    ("Functions", "functions"),
    ("Loops", "loops"),
    ("Components", "components"),
    ("Setup / Tooling", "setup-tooling"),
    ("HTTP / API", "http-api"),
    ("Debugging", "debugging"),
    ("Strings", "strings"),
    ("Data Transform", "data-transform"),
]


def seed_if_empty(db: Session) -> None:
    platform_count = db.query(Platform).count()
    topic_count = db.query(Topic).count()

    if platform_count == 0:
        for name, slug, typ in DEFAULT_PLATFORMS:
            db.add(Platform(name=name, slug=slug, type=typ))

    if topic_count == 0:
        for name, slug in DEFAULT_TOPICS:
            db.add(Topic(name=name, slug=slug))

    if platform_count == 0 or topic_count == 0:
        db.commit()
