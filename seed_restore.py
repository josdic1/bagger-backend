# seed_restore.py
import json
import os
from sqlalchemy import text

from database import SessionLocal
from models.user import User
from models.platform import Platform
from models.topic import Topic
from models.cheat import Cheat, CheatPlatform, CheatTopic
from models.user_cheat import UserCheat

DATA_PATH = os.path.join(os.path.dirname(__file__), "seed_data.json")


def pick(d: dict, keys: set[str]) -> dict:
    return {k: d[k] for k in keys if k in d}


def _load():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _truncate_all(db):
    dialect = db.bind.dialect.name  # "sqlite" or "postgresql"

    if dialect == "postgresql":
        db.execute(
            text(
                "TRUNCATE TABLE user_cheats, cheat_topics, cheat_platforms, cheats, topics, platforms, users RESTART IDENTITY CASCADE;"
            )
        )
        return

    if dialect == "sqlite":
        db.execute(text("PRAGMA foreign_keys=OFF;"))

        existing = {
            row[0]
            for row in db.execute(
                text("SELECT name FROM sqlite_master WHERE type='table';")
            ).fetchall()
        }

        for table in [
            "user_cheats",
            "cheat_topics",
            "cheat_platforms",
            "cheats",
            "topics",
            "platforms",
            "users",
        ]:
            if table in existing:
                db.execute(text(f"DELETE FROM {table};"))

        if "sqlite_sequence" in existing:
            db.execute(text("DELETE FROM sqlite_sequence;"))

        db.execute(text("PRAGMA foreign_keys=ON;"))
        return

    raise RuntimeError(f"Unsupported DB dialect: {dialect}")


def _reset_seq(db, table, id_col="id"):
    # Postgres only. SQLite reset handled in _truncate_all via sqlite_sequence.
    if db.bind.dialect.name != "postgresql":
        return

    db.execute(
        text(
            f"""
            SELECT setval(
              pg_get_serial_sequence('{table}', '{id_col}'),
              COALESCE((SELECT MAX({id_col}) FROM {table}), 1),
              true
            );
            """
        )
    )


def restore_snapshot():
    data = _load()

    ALLOWED_USER_KEYS = {
        "id",
        "email",
        "name",
        "password_hash",
        "is_admin",
        "created_at",
        "updated_at",
    }

    ALLOWED_CHEAT_KEYS = {
        "id",
        "title",
        "code",
        "notes",
        "created_by_user_id",
        "is_public",
        "created_at",
        "updated_at",
    }

    db = SessionLocal()
    try:
        _truncate_all(db)

        # USERS
        for u in data.get("users", []):
            db.add(User(**pick(u, ALLOWED_USER_KEYS)))

        # PLATFORMS
        for p in data.get("platforms", []):
            db.add(Platform(**p))

        # TOPICS
        for t in data.get("topics", []):
            db.add(Topic(**t))

        db.flush()

        # CHEATS (strip metadata_tag etc)
        for c in data.get("cheats", []):
            db.add(Cheat(**pick(c, ALLOWED_CHEAT_KEYS)))

        db.flush()

        # JOIN TABLES
        for cp in data.get("cheat_platforms", []):
            db.add(CheatPlatform(**cp))

        for ct in data.get("cheat_topics", []):
            db.add(CheatTopic(**ct))

        for uc in data.get("user_cheats", []):
            db.add(UserCheat(**uc))

        db.commit()

        # reset sequences so future inserts don’t collide
        _reset_seq(db, "users")
        _reset_seq(db, "platforms")
        _reset_seq(db, "topics")
        _reset_seq(db, "cheats")
        db.commit()

        print("✅ Snapshot restored.")
    finally:
        db.close()


if __name__ == "__main__":
    restore_snapshot()
