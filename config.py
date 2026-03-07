from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(slots=True)
class Settings:
    bot_token: str
    database_url: str
    default_timezone: str

    @classmethod
    def from_env(cls) -> "Settings":
        token = os.getenv("BOT_TOKEN", "").strip()
        if not token:
            raise ValueError("BOT_TOKEN is not set in environment")
        return cls(
            bot_token=token,
            database_url=os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./habit_tracker.db"),
            default_timezone=os.getenv("DEFAULT_TIMEZONE", "Europe/Moscow"),
        )
