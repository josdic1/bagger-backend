# seed_restore.py
import json
import os
from sqlalchemy import text
from database import SessionLocal  # must be your prod SessionLocal

from models.user import User
from models.platform import Platform
from models.topic import Topic
from models.cheat import Cheat, CheatPlatform, CheatTopic
from models.user_cheat import UserCheat  # if you have it


DATA_PATH = os.path.join(os.path.dirname(__file__), "seed_data.json")


def _load():
  with open(DATA_PATH, "r", encoding="utf-8") as f:
    return json.load(f)


def _truncate_all(db):
  # Postgres-safe: wipe everything and restart ids
  db.execute(text("TRUNCATE TABLE user_cheats, cheat_topics, cheat_platforms, cheats, topics, platforms, users RESTART IDENTITY CASCADE;"))


def _reset_seq(db, table, id_col="id"):
  # Fix sequences after explicit-id inserts
  db.execute(text(f"""
    SELECT setval(
      pg_get_serial_sequence('{table}', '{id_col}'),
      COALESCE((SELECT MAX({id_col}) FROM {table}), 1),
      true
    );
  """))


def restore_snapshot():
  data = _load()

  db = SessionLocal()
  try:
    _truncate_all(db)

    # USERS
    for u in data.get("users", []):
      db.add(User(**u))

    # PLATFORMS
    for p in data.get("platforms", []):

      db.add(Platform(**p))
    # TOPICS
    for t in data.get("topics", []):
      db.add(Topic(**t))

    db.flush()

    # CHEATS
    for c in data.get("cheats", []):
      db.add(Cheat(**c))

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
