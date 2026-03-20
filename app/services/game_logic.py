from __future__ import annotations

import random
from dataclasses import dataclass

from app.models.enums import GameStatus, StartupNiche


@dataclass(slots=True)
class ActionOutcome:
    text: str
    game_over: bool = False
    outcome_title: str | None = None


NICHE_BONUSES: dict[StartupNiche, dict[str, int]] = {
    StartupNiche.EDTECH: {"reputation": 5, "product_level": 1},
    StartupNiche.FOODTECH: {"clients": 20, "marketing_level": 1},
    StartupNiche.ECOTECH: {"reputation": 8, "risk": -2},
    StartupNiche.GAMEDEV: {"product_level": 2, "risk": 3},
    StartupNiche.FINTECH: {"money": 15000, "risk": 5},
}

EVENTS = [
    ("Удачная реклама принесла волну новых заявок.", {"clients": 45, "reputation": 4}),
    ("Негативный отзыв снизил доверие к бренду.", {"reputation": -7, "risk": 4}),
    ("На рынок вышел сильный конкурент.", {"risk": 8}),
    ("Вирусный пост взорвал соцсети.", {"clients": 80, "reputation": 6}),
    ("Сбой в продукте ударил по репутации.", {"reputation": -8, "risk": 6}),
    ("Инвестор сам написал вам после новости о росте.", {"money": 25000, "reputation": 3}),
    ("Партнёрство с локальным брендом привело новых клиентов.", {"clients": 60, "money": 12000}),
    ("Команда выгорела после тяжёлого спринта.", {"team_level": -1, "risk": 5}),
    ("Успешное обновление продукта порадовало пользователей.", {"product_level": 1, "reputation": 5}),
    ("Экономический кризис увеличил стоимость привлечения.", {"money": -15000, "risk": 7}),
    ("Выступление на конференции принесло известность.", {"reputation": 7, "clients": 30}),
    ("Ошибка в найме замедлила процессы.", {"money": -8000, "team_level": -1}),
    ("Новый корпоративный клиент купил подписку.", {"money": 30000, "clients": 50}),
    ("Грантовая программа поддержала ваш проект.", {"money": 20000, "reputation": 4}),
    ("Неудачный релиз вызвал волну отмен.", {"clients": -35, "reputation": -6}),
    ("Сильный PR-кейс повысил узнаваемость.", {"marketing_level": 1, "reputation": 5}),
    ("Случился кассовый разрыв по платежам.", {"money": -12000}),
    ("Команда предложила инновационную фичу.", {"product_level": 1, "clients": 20}),
    ("Фонд акселератора дал полезные контакты.", {"reputation": 4, "clients": 35}),
    ("Сервис-партнёр поднял цены на интеграцию.", {"money": -10000, "risk": 4}),
]


def clamp(game) -> None:
    game.money = max(game.money, -999999)
    game.reputation = max(min(game.reputation, 100), 0)
    game.clients = max(game.clients, 0)
    game.product_level = max(game.product_level, 1)
    game.team_level = max(game.team_level, 1)
    game.marketing_level = max(game.marketing_level, 1)
    game.risk = max(min(game.risk, 100), 0)
    game.turns = max(game.turns, 0)


def initial_stats(niche: StartupNiche) -> dict[str, int | str]:
    stats: dict[str, int | str] = {
        "money": 100000,
        "reputation": 20,
        "clients": 10,
        "product_level": 1,
        "team_level": 1,
        "marketing_level": 1,
        "turns": 30,
        "risk": 10,
        "current_day": 1,
        "game_status": GameStatus.ACTIVE,
    }
    for key, value in NICHE_BONUSES[niche].items():
        stats[key] = int(stats.get(key, 0)) + value
    return stats


def format_stats(game, upgrades: list[str] | None = None) -> str:
    upgrades_text = ", ".join(upgrades) if upgrades else "нет"
    return (
        f"📊 *{game.startup_name}* ({game.startup_niche.value})\n"
        f"День: {game.current_day}/30\n"
        f"Деньги: {game.money:,} ₽\n"
        f"Репутация: {game.reputation}/100\n"
        f"Клиенты: {game.clients}\n"
        f"Продукт: {game.product_level}\n"
        f"Команда: {game.team_level}\n"
        f"Маркетинг: {game.marketing_level}\n"
        f"Риск: {game.risk}/100\n"
        f"Осталось ходов: {game.turns}\n"
        f"Статус: {game.game_status.value}\n"
        f"Улучшения: {upgrades_text}"
    )


def calculate_score(game) -> int:
    return max(0, game.money // 1000 + game.clients * 2 + game.reputation * 15 + game.product_level * 40 + game.team_level * 35 + game.marketing_level * 30 - game.risk * 10)


def apply_action(game, action: str) -> str:
    if action == "product":
        cost = 12000 + game.product_level * 2000
        gain = random.randint(1, 2)
        rep = random.randint(1, 4)
        clients = random.randint(0, 20 + game.team_level * 5)
        game.money -= cost
        game.product_level += gain
        game.reputation += rep
        game.clients += clients
        game.risk -= 2
        text = f"🛠 Продукт улучшен: -{cost:,} ₽, +{gain} к продукту, +{rep} к репутации, +{clients} клиентов."
    elif action == "marketing":
        cost = 10000 + game.marketing_level * 1500
        multiplier = random.choice([0.7, 1.0, 1.4, 1.8])
        clients = int((25 + game.marketing_level * 12) * multiplier)
        rep = random.randint(0, 3)
        game.money -= cost
        game.marketing_level += 1
        game.clients += clients
        game.reputation += rep
        game.risk += 1
        text = f"📣 Реклама запущена: -{cost:,} ₽, +1 к маркетингу, +{clients} клиентов, +{rep} к репутации."
    elif action == "hire":
        cost = 15000 + game.team_level * 3000
        game.money -= cost
        game.team_level += 1
        game.risk -= random.randint(2, 5)
        text = f"👥 Новый сотрудник в команде: -{cost:,} ₽, +1 к команде, риск снижен."
    elif action == "consult":
        cost = 7000
        boosts = ["product_level", "team_level", "marketing_level", "reputation"]
        stat = random.choice(boosts)
        value = 2 if stat == "reputation" else 1
        setattr(game, stat, getattr(game, stat) + value)
        game.money -= cost
        tips = {
            "product_level": "Сфокусируйтесь на главной боли клиента.",
            "team_level": "Нанимайте медленно, увольняйте быстро.",
            "marketing_level": "Сначала проверьте канал на маленьком бюджете.",
            "reputation": "Показывайте кейсы и отзывы чаще.",
        }
        text = f"🎓 Консультация оплачена: -{cost:,} ₽. Улучшен параметр {stat}. Совет: {tips[stat]}"
    elif action == "investor":
        chance = 35 + game.reputation // 2 + game.product_level * 5 + game.clients // 40
        roll = random.randint(1, 100)
        if roll <= min(chance, 85):
            investment = 30000 + game.product_level * 8000 + game.team_level * 5000
            game.money += investment
            game.reputation += 4
            text = f"💼 Инвестор поверил в стартап. Получено {investment:,} ₽ и +4 к репутации."
        else:
            rep_loss = random.randint(2, 6)
            game.reputation -= rep_loss
            game.risk += 3
            text = f"🙅 Питч провалился. Репутация -{rep_loss}, риск вырос."
    else:
        text = "Неизвестное действие."
    clamp(game)
    return text


def advance_day(game) -> str:
    base_income = game.clients * (15 + game.product_level * 2)
    salary_cost = game.team_level * 3500
    marketing_burn = game.marketing_level * 1000
    game.money += base_income - salary_cost - marketing_burn
    game.reputation += 1 if game.product_level >= 3 else 0
    game.clients += max(0, game.marketing_level * 5 + game.reputation // 10 - game.risk // 20)
    event_text, effects = random.choice(EVENTS)
    for key, value in effects.items():
        setattr(game, key, getattr(game, key) + value)
    game.current_day += 1
    game.turns -= 1
    clamp(game)
    return f"⏭ День завершён. Доход/расходы пересчитаны. Событие дня: {event_text}"


def check_game_status(game) -> ActionOutcome:
    if game.money <= 0:
        game.game_status = GameStatus.LOST
        return ActionOutcome("💸 Стартап обанкротился: деньги закончились.", True, "Поражение")
    if game.risk >= 100:
        game.game_status = GameStatus.LOST
        return ActionOutcome("⚠️ Риск вышел из-под контроля. Инвесторы и клиенты ушли.", True, "Поражение")
    if game.reputation <= 0:
        game.game_status = GameStatus.LOST
        return ActionOutcome("📉 Репутация разрушена. Рынок вам больше не доверяет.", True, "Поражение")
    if game.clients >= 1000 or (game.reputation >= 90 and game.money >= 500000):
        game.game_status = GameStatus.WON
        return ActionOutcome("🏆 Стартап стал заметным успехом на рынке!", True, "Победа")
    if game.turns <= 0 or game.current_day > 30:
        score = calculate_score(game)
        if score >= 1200:
            game.game_status = GameStatus.WON
            return ActionOutcome(f"🎯 Вы дошли до финала акселератора. Итоговый score: {score}.", True, "Победа")
        game.game_status = GameStatus.LOST
        return ActionOutcome(f"⌛ Время закончилось. Итоговый score: {score}.", True, "Поражение")
    return ActionOutcome("Игра продолжается.")
