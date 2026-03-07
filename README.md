# Telegram Video Saver Bot (aiogram)

Бот сохраняет ссылки на видео, умеет отмечать просмотренные, добавлять в избранное и плейлисты, делать AI-резюме YouTube-видео и ставить напоминания.

## Установка

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Заполните `.env`:
- `BOT_TOKEN`
- `OPENAI_API_KEY`
- `OPENAI_MODEL` (опционально)
- `DATABASE_PATH` (опционально)

## Запуск

```bash
python -m bot.bot
```

## Получение Telegram Bot Token
1. Откройте Telegram и найдите `@BotFather`.
2. Отправьте команду `/newbot`.
3. Укажите имя бота и username (должен оканчиваться на `bot`).
4. BotFather вернёт токен — скопируйте его в `.env` как `BOT_TOKEN`.

## Структура проекта

```text
bot/
    __init__.py
    bot.py
    handlers.py
    database.py
    keyboards.py
    playlists.py
    ai_summary.py
    reminders.py
    config.py
.env.example
requirements.txt
README.md
```
