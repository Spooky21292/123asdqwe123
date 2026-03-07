import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
from openai import OpenAI

# Загружаем переменные из .env файла (ключи хранятся там)
load_dotenv()

# Берём токены из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден. Добавьте его в файл .env")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY не найден. Добавьте его в файл .env")

# Создаём Telegram-бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаём клиент OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)


@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    """Обработчик команды /start."""
    await message.answer(
        "Привет! Я простой бот с ChatGPT. "
        "Напиши любой текст, и я отвечу."
    )


@dp.message()
async def chat_handler(message: Message) -> None:
    """Обработчик любых сообщений пользователя."""
    user_text = message.text or ""

    try:
        # Отправляем сообщение пользователя в OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Ты дружелюбный помощник и отвечаешь на русском языке.",
                },
                {"role": "user", "content": user_text},
            ],
        )

        # Берём текст ответа модели
        answer = response.choices[0].message.content or "Пустой ответ от модели."

        # Отправляем ответ обратно в Telegram
        await message.answer(answer)
    except Exception as error:
        await message.answer(f"Ошибка при запросе к OpenAI: {error}")


async def main() -> None:
    """Запуск бота через polling (без webhook)."""
    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Как запускать:
    # 1) pip install -r requirements.txt
    # 2) создать .env на основе .env.example и вставить ключи
    # 3) python bot.py
    asyncio.run(main())
