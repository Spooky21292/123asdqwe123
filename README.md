# Habit Tracker Telegram Bot (MVP)

Рабочий Telegram-бот на **Python 3.12 + aiogram 3.x**, который помогает вести привычки, отмечать выполнение, считать стрики, хранить цели/заметки и отправлять напоминания.

## Структура проекта

```text
.
├── bot.py
├── config.py
├── requirements.txt
├── .env.example
├── database/
│   ├── base.py
│   ├── models.py
│   └── session.py
├── handlers/
│   ├── errors.py
│   ├── goals.py
│   ├── habits.py
│   ├── marking.py
│   ├── notes.py
│   ├── settings.py
│   └── start.py
├── keyboards/
│   ├── inline.py
│   └── reply.py
├── repositories/
│   ├── goals.py
│   ├── habits.py
│   ├── notes.py
│   └── users.py
├── scheduler/
│   └── reminders.py
├── services/
│   └── habit_service.py
├── states/
│   ├── goal.py
│   ├── habit.py
│   ├── note.py
│   └── settings.py
└── utils/
    └── datetime_utils.py
```

## Что уже реализовано

### Привычки (основной фокус)
- добавление привычки через FSM: название, описание, частота, напоминания;
- частота: каждый день или выбранные дни недели;
- просмотр, удаление, включение/отключение привычки;
- ежедневная отметка статуса через inline-кнопки: ✅/❌/⏰;
- обновление статуса за текущий день без дублирования записи;
- корректный расчёт стриков по каждой привычке, включая привычки по дням недели;
- статистика за 7/30 дней + текущий/лучший стрик + total done.

### Дополнительно
- регистрация пользователя при `/start`;
- разделы целей и заметок (MVP-функции);
- настройки: timezone, глобальное включение/выключение напоминаний;
- напоминания через APScheduler;
- автосоздание таблиц SQLite при старте.

## Быстрый запуск

### 1) Подготовь окружение
Linux/macOS:
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2) Настрой `.env`
```bash
cp .env.example .env
```
Вставь токен Telegram-бота в `BOT_TOKEN`.

### 3) Запусти
```bash
python bot.py
```

## Основные команды и сценарии
- `/start` — регистрация и приветствие;
- кнопка **Добавить привычку** — запуск FSM создания привычки;
- кнопка **Отметить сегодня** — быстрые ежедневные отметки;
- кнопка **Статистика** — метрики по привычке;
- `/add_goal` — добавить цель;
- `/add_note` — добавить заметку;
- `/timezone` — изменить часовой пояс;
- `/toggle_reminders` — включить/выключить напоминания глобально.

## Примечания
- База: SQLite (`habit_tracker.db`), ORM: SQLAlchemy async;
- Для reminders бот проверяет привычки каждую минуту и отправляет напоминания в заданное локальное время пользователя.


## Если видишь ошибку `BOT_TOKEN is not set`
1. Убедись, что файл `.env` лежит рядом с `bot.py` (в корне проекта).
2. Убедись, что в `.env` есть строка без кавычек и пробелов вокруг `=`:
```env
BOT_TOKEN=your_telegram_bot_token
```
3. Перезапусти бота после изменения `.env`.


## Если видишь ошибку `greenlet library is required`
Это значит, что не установилась зависимость `greenlet`, которая нужна SQLAlchemy async.

Сделай в активированном venv:
```bash
pip install -r requirements.txt
```

Если ошибка осталась:
```bash
pip install greenlet==3.1.1
```
