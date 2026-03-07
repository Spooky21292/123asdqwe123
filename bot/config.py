from dataclasses import dataclass
import os
from dotenv import load_dotenv


load_dotenv()


@dataclass(slots=True)
class Settings:
    bot_token: str
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    database_path: str = "videos.db"



def get_settings() -> Settings:
    bot_token = os.getenv("BOT_TOKEN", "")
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    database_path = os.getenv("DATABASE_PATH", "videos.db")

    if not bot_token:
        raise ValueError("BOT_TOKEN is not set")

    return Settings(
        bot_token=bot_token,
        openai_api_key=openai_api_key,
        openai_model=openai_model,
        database_path=database_path,
    )
