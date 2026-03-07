from __future__ import annotations

from datetime import date, datetime, time
from enum import Enum

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    Time,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class FrequencyType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"


class HabitStatus(str, Enum):
    DONE = "done"
    MISSED = "missed"
    LATER = "later"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    timezone: Mapped[str] = mapped_column(String(64), default="Europe/Moscow")
    reminders_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    habits: Mapped[list[Habit]] = relationship(back_populates="user", cascade="all, delete-orphan")
    goals: Mapped[list[Goal]] = relationship(back_populates="user", cascade="all, delete-orphan")
    notes: Mapped[list[Note]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    frequency_type: Mapped[FrequencyType] = mapped_column(SAEnum(FrequencyType), default=FrequencyType.DAILY)
    days_of_week: Mapped[str | None] = mapped_column(String(32), nullable=True)
    reminder_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    reminder_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped[User] = relationship(back_populates="habits")
    logs: Mapped[list[HabitLog]] = relationship(back_populates="habit", cascade="all, delete-orphan")

    __table_args__ = (Index("ix_habits_user_active", "user_id", "is_active"),)


class HabitLog(Base):
    __tablename__ = "habit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    log_date: Mapped[date] = mapped_column(Date)
    status: Mapped[HabitStatus] = mapped_column(SAEnum(HabitStatus))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    habit: Mapped[Habit] = relationship(back_populates="logs")

    __table_args__ = (
        UniqueConstraint("habit_id", "log_date", name="uq_habit_log_date"),
        Index("ix_logs_habit_date", "habit_id", "log_date"),
    )


class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped[User] = relationship(back_populates="goals")


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped[User] = relationship(back_populates="notes")
