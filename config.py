from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
DOTENV_PATH = BASE_DIR / ".env"

# Явно подгружаем .env из корня проекта, чтобы одинаково работало в IDE/Windows/Linux.
load_dotenv(dotenv_path=DOTENV_PATH)


@dataclass(slots=True)
class Settings:
    bot_token: str
    database_url: str
    default_timezone: str

    @classmethod
    def from_env(cls) -> "Settings":
        token = os.getenv("BOT_TOKEN", "").strip()
        if not token:
            raise ValueError(
                "BOT_TOKEN is not set. Create .env in project root and add line: "
                "BOT_TOKEN=your_telegram_bot_token"
            )
        return cls(
            bot_token=token,
            database_url=os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./habit_tracker.db"),
            default_timezone=os.getenv("DEFAULT_TIMEZONE", "Europe/Moscow"),
        )
