from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Platform(Base):
    __tablename__ = "platforms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False, default="language")  # language/framework/tool/format

    cheat_links = relationship("CheatPlatform", back_populates="platform", cascade="all, delete-orphan")
