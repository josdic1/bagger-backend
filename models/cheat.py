from sqlalchemy import String, Integer, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from typing import Optional, List
from database import Base


class Cheat(Base):
    __tablename__ = "cheats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    code: Mapped[str] = mapped_column(Text, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # who created this cheat (nullable if you seed as "system")
    created_by_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)

    is_public: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    created_by = relationship("User", back_populates="cheats")

    platforms: Mapped[List["CheatPlatform"]] = relationship(
        "CheatPlatform", back_populates="cheat", cascade="all, delete-orphan"
    )
    topics: Mapped[List["CheatTopic"]] = relationship(
        "CheatTopic", back_populates="cheat", cascade="all, delete-orphan"
    )

    user_overlays = relationship("UserCheat", back_populates="cheat", cascade="all, delete-orphan")


class CheatPlatform(Base):
    __tablename__ = "cheat_platforms"

    cheat_id: Mapped[int] = mapped_column(ForeignKey("cheats.id"), primary_key=True)
    platform_id: Mapped[int] = mapped_column(ForeignKey("platforms.id"), primary_key=True)

    cheat = relationship("Cheat", back_populates="platforms")
    platform = relationship("Platform", back_populates="cheat_links")


class CheatTopic(Base):
    __tablename__ = "cheat_topics"

    cheat_id: Mapped[int] = mapped_column(ForeignKey("cheats.id"), primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"), primary_key=True)

    cheat = relationship("Cheat", back_populates="topics")
    topic = relationship("Topic", back_populates="cheat_links")
