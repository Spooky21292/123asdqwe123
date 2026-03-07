from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from database.models import FrequencyType, Habit, HabitStatus
from repositories.habits import HabitRepository
from utils.datetime_utils import local_today, parse_days


@dataclass(slots=True)
class HabitStats:
    done_7: int
    total_7: int
    done_30: int
    total_30: int
    current_streak: int
    best_streak: int
    total_done: int


class HabitService:
    def __init__(self, habit_repo: HabitRepository) -> None:
        self.habit_repo = habit_repo

    @staticmethod
    def is_habit_scheduled_for_date(habit: Habit, target_date: date) -> bool:
        if habit.frequency_type == FrequencyType.DAILY:
            return True
        active_days = parse_days(habit.days_of_week)
        return target_date.weekday() in active_days

    async def habits_for_today(self, user_id: int, timezone: str) -> list[Habit]:
        today = local_today(timezone)
        habits = await self.habit_repo.get_user_habits(user_id=user_id, active_only=True)
        return [habit for habit in habits if self.is_habit_scheduled_for_date(habit, today)]

    async def calculate_streak(self, habit: Habit, timezone: str) -> tuple[int, int]:
        today = local_today(timezone)
        start_date = today - timedelta(days=365)
        logs = await self.habit_repo.get_logs_for_period(habit.id, start_date, today)
        log_by_date = {log.log_date: log.status for log in logs}

        scheduled_dates = [
            day
            for i in range(366)
            if self.is_habit_scheduled_for_date(habit, (day := today - timedelta(days=i)))
        ]

        current = 0
        for day in scheduled_dates:
            status = log_by_date.get(day)
            if status == HabitStatus.DONE:
                current += 1
            elif status in {HabitStatus.MISSED}:
                break
            else:
                if day != today:
                    break

        best = 0
        running = 0
        for day in reversed(scheduled_dates):
            status = log_by_date.get(day)
            if status == HabitStatus.DONE:
                running += 1
                best = max(best, running)
            else:
                running = 0

        return current, best

    async def calculate_stats(self, habit: Habit, timezone: str) -> HabitStats:
        today = local_today(timezone)

        def period_stats(days: int) -> tuple[int, list[date]]:
            start = today - timedelta(days=days - 1)
            scheduled = [
                start + timedelta(days=i)
                for i in range(days)
                if self.is_habit_scheduled_for_date(habit, start + timedelta(days=i))
            ]
            return len(scheduled), scheduled

        total_7, scheduled_7 = period_stats(7)
        total_30, scheduled_30 = period_stats(30)

        logs = await self.habit_repo.get_logs_for_period(habit.id, today - timedelta(days=29), today)
        log_by_date = {log.log_date: log.status for log in logs}

        done_7 = sum(1 for d in scheduled_7 if log_by_date.get(d) == HabitStatus.DONE)
        done_30 = sum(1 for d in scheduled_30 if log_by_date.get(d) == HabitStatus.DONE)
        current_streak, best_streak = await self.calculate_streak(habit, timezone)
        total_done = await self.habit_repo.get_done_count(habit.id)

        return HabitStats(
            done_7=done_7,
            total_7=total_7,
            done_30=done_30,
            total_30=total_30,
            current_streak=current_streak,
            best_streak=best_streak,
            total_done=total_done,
        )
