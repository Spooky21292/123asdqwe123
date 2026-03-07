from datetime import date, datetime, time

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import FrequencyType, Habit, HabitLog, HabitStatus


class HabitRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_habit(
        self,
        user_id: int,
        title: str,
        description: str | None,
        frequency_type: FrequencyType,
        days_of_week: str | None,
        reminder_enabled: bool,
        reminder_time: time | None,
    ) -> Habit:
        habit = Habit(
            user_id=user_id,
            title=title,
            description=description,
            frequency_type=frequency_type,
            days_of_week=days_of_week,
            reminder_enabled=reminder_enabled,
            reminder_time=reminder_time,
        )
        self.session.add(habit)
        await self.session.commit()
        await self.session.refresh(habit)
        return habit

    async def get_user_habits(self, user_id: int, active_only: bool = False) -> list[Habit]:
        query = select(Habit).where(Habit.user_id == user_id).order_by(Habit.created_at.desc())
        if active_only:
            query = query.where(Habit.is_active.is_(True))
        result = await self.session.scalars(query)
        return list(result)

    async def get_by_id(self, habit_id: int, user_id: int) -> Habit | None:
        query = select(Habit).where(and_(Habit.id == habit_id, Habit.user_id == user_id))
        return await self.session.scalar(query)

    async def delete(self, habit: Habit) -> None:
        await self.session.delete(habit)
        await self.session.commit()

    async def set_active(self, habit: Habit, is_active: bool) -> Habit:
        habit.is_active = is_active
        await self.session.commit()
        await self.session.refresh(habit)
        return habit

    async def update_reminder_time(self, habit: Habit, reminder_time: time) -> Habit:
        habit.reminder_time = reminder_time
        habit.reminder_enabled = True
        await self.session.commit()
        await self.session.refresh(habit)
        return habit

    async def upsert_log(self, habit_id: int, user_id: int, log_date: date, status: HabitStatus) -> HabitLog:
        query = select(HabitLog).where(and_(HabitLog.habit_id == habit_id, HabitLog.log_date == log_date))
        log = await self.session.scalar(query)
        if log:
            log.status = status
            log.updated_at = datetime.utcnow()
        else:
            log = HabitLog(habit_id=habit_id, user_id=user_id, log_date=log_date, status=status)
            self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)
        return log

    async def get_log(self, habit_id: int, log_date: date) -> HabitLog | None:
        query = select(HabitLog).where(and_(HabitLog.habit_id == habit_id, HabitLog.log_date == log_date))
        return await self.session.scalar(query)

    async def get_logs_for_period(self, habit_id: int, start_date: date, end_date: date) -> list[HabitLog]:
        query = (
            select(HabitLog)
            .where(and_(HabitLog.habit_id == habit_id, HabitLog.log_date >= start_date, HabitLog.log_date <= end_date))
            .order_by(HabitLog.log_date.desc())
        )
        result = await self.session.scalars(query)
        return list(result)

    async def get_done_count(self, habit_id: int) -> int:
        query = select(func.count(HabitLog.id)).where(
            and_(HabitLog.habit_id == habit_id, HabitLog.status == HabitStatus.DONE)
        )
        return int((await self.session.scalar(query)) or 0)

    async def habits_for_reminders(self) -> list[Habit]:
        query = select(Habit).where(
            and_(Habit.is_active.is_(True), Habit.reminder_enabled.is_(True), Habit.reminder_time.is_not(None))
        )
        result = await self.session.scalars(query)
        return list(result)
