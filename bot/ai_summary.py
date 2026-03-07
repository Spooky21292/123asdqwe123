from __future__ import annotations

import re
from urllib.parse import parse_qs, urlparse

from openai import AsyncOpenAI
from youtube_transcript_api import YouTubeTranscriptApi


YOUTUBE_DOMAINS = {"youtube.com", "www.youtube.com", "youtu.be", "m.youtube.com"}


def extract_youtube_video_id(url: str) -> str | None:
    parsed = urlparse(url)
    host = parsed.netloc.lower()

    if host == "youtu.be":
        return parsed.path.strip("/") or None

    if host in YOUTUBE_DOMAINS:
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]
        match = re.match(r"^/(shorts|embed)/([^/?]+)", parsed.path)
        if match:
            return match.group(2)

    return None


async def build_video_summary(url: str, api_key: str, model: str = "gpt-4o-mini") -> str:
    video_id = extract_youtube_video_id(url)
    if not video_id:
        return "Резюме доступно только для YouTube-ссылок с корректным ID видео."

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["ru", "en"])
    except Exception as exc:  # noqa: BLE001
        return f"Не удалось получить транскрипт: {exc}"

    transcript_text = " ".join(item["text"] for item in transcript)
    if not transcript_text.strip():
        return "Транскрипт пустой, поэтому резюме сформировать не удалось."

    if not api_key:
        return "OPENAI_API_KEY не настроен. Добавьте ключ в .env, чтобы получать AI-резюме."

    client = AsyncOpenAI(api_key=api_key)
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Ты делаешь очень краткие и структурированные резюме видео на русском языке.",
            },
            {
                "role": "user",
                "content": (
                    "Сделай краткое резюме транскрипта видео в формате:\n"
                    "- главная идея\n- ключевые моменты\n- вывод\n\n"
                    f"Транскрипт:\n{transcript_text[:12000]}"
                ),
            },
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content or "AI не вернул текст резюме."
