from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Upgrade(Base):
    __tablename__ = "upgrades"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(Text)
    cost: Mapped[int] = mapped_column(Integer)
    money_bonus: Mapped[int] = mapped_column(Integer, default=0)
    reputation_bonus: Mapped[int] = mapped_column(Integer, default=0)
    clients_bonus: Mapped[int] = mapped_column(Integer, default=0)
    product_bonus: Mapped[int] = mapped_column(Integer, default=0)
    team_bonus: Mapped[int] = mapped_column(Integer, default=0)
    marketing_bonus: Mapped[int] = mapped_column(Integer, default=0)
    risk_bonus: Mapped[int] = mapped_column(Integer, default=0)
    one_time: Mapped[bool] = mapped_column(Boolean, default=True)

    user_upgrades = relationship("UserUpgrade", back_populates="upgrade")


class UserUpgrade(Base):
    __tablename__ = "user_upgrades"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id", ondelete="CASCADE"), index=True)
    upgrade_id: Mapped[int] = mapped_column(ForeignKey("upgrades.id", ondelete="CASCADE"), index=True)

    game = relationship("Game", back_populates="user_upgrades")
    upgrade = relationship("Upgrade", back_populates="user_upgrades")
