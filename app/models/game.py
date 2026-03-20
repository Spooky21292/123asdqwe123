from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.enums import GameStatus, StartupNiche


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    startup_name: Mapped[str] = mapped_column(String(120))
    startup_niche: Mapped[StartupNiche] = mapped_column(SqlEnum(StartupNiche))
    money: Mapped[int] = mapped_column(Integer, default=100000)
    reputation: Mapped[int] = mapped_column(Integer, default=20)
    clients: Mapped[int] = mapped_column(Integer, default=0)
    product_level: Mapped[int] = mapped_column(Integer, default=1)
    team_level: Mapped[int] = mapped_column(Integer, default=1)
    marketing_level: Mapped[int] = mapped_column(Integer, default=1)
    turns: Mapped[int] = mapped_column(Integer, default=30)
    risk: Mapped[int] = mapped_column(Integer, default=10)
    current_day: Mapped[int] = mapped_column(Integer, default=1)
    game_status: Mapped[GameStatus] = mapped_column(SqlEnum(GameStatus), default=GameStatus.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="games")
    user_upgrades = relationship("UserUpgrade", back_populates="game", cascade="all, delete-orphan")
