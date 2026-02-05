from sqlalchemy import Integer, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from typing import Optional
from database import Base


class UserCheat(Base):
    """
    User-specific overlay for any cheat:
    - favorites
    - personal notes
    - optional custom title later
    """
    __tablename__ = "user_cheats"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    cheat_id: Mapped[int] = mapped_column(ForeignKey("cheats.id"), primary_key=True)

    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    personal_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user = relationship("User", back_populates="user_cheats")
    cheat = relationship("Cheat", back_populates="user_overlays")
