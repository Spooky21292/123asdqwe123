from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import os

from dotenv import load_dotenv


@dataclass(slots=True)
class Settings:
    bot_token: str
    admin_id: int
    database_url: str
    log_level: str = "INFO"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    load_dotenv()
    token = os.getenv("BOT_TOKEN", "").strip()
    admin_id_raw = os.getenv("ADMIN_ID", "0").strip()
    database_url = os.getenv(
        "DATABASE_URL", "sqlite+aiosqlite:///./startup_simulator.db"
    ).strip()

    if not token:
        raise ValueError("BOT_TOKEN is not set in environment.")

    try:
        admin_id = int(admin_id_raw)
    except ValueError as exc:
        raise ValueError("ADMIN_ID must be an integer.") from exc

    return Settings(
        bot_token=token,
        admin_id=admin_id,
        database_url=database_url,
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
    )
