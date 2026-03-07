from __future__ import annotations

from datetime import date, datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


WEEKDAY_NAMES = {
    0: "Пн",
    1: "Вт",
    2: "Ср",
    3: "Чт",
    4: "Пт",
    5: "Сб",
    6: "Вс",
}


def parse_timezone(timezone_name: str, fallback: str = "Europe/Moscow") -> ZoneInfo:
    try:
        return ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError:
        return ZoneInfo(fallback)


def local_today(timezone_name: str) -> date:
    return datetime.now(parse_timezone(timezone_name)).date()


def parse_days(days_string: str | None) -> set[int]:
    if not days_string:
        return set()
    return {int(item) for item in days_string.split(",") if item.strip().isdigit()}


def format_days(days_string: str | None) -> str:
    days = sorted(parse_days(days_string))
    if not days:
        return "Каждый день"
    return ", ".join(WEEKDAY_NAMES.get(day, str(day)) for day in days)
