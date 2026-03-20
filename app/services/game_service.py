from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories import GameRepository, ResultRepository, UpgradeRepository, UserRepository
from app.models import GameResult
from app.models.enums import StartupNiche
from app.services.game_logic import ActionOutcome, advance_day, apply_action, calculate_score, check_game_status, format_stats, initial_stats

logger = logging.getLogger(__name__)


class GameService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(session)
        self.games = GameRepository(session)
        self.upgrades = UpgradeRepository(session)
        self.results = ResultRepository(session)

    async def register_user(self, telegram_id: int, username: str | None, full_name: str):
        return await self.users.get_or_create_user(telegram_id, username, full_name)

    async def create_new_game(self, user_id: int, startup_name: str, niche: StartupNiche):
        stats = initial_stats(niche)
        return await self.games.create_game(user_id=user_id, startup_name=startup_name, startup_niche=niche, **stats)

    async def get_active_game(self, user_id: int):
        return await self.games.get_active_game(user_id)

    async def get_profile_text(self, game) -> str:
        upgrades = [item.upgrade.name for item in game.user_upgrades]
        return format_stats(game, upgrades)

    async def do_action(self, game, action: str) -> tuple[str, ActionOutcome]:
        text = apply_action(game, action)
        await self.games.save(game)
        status = check_game_status(game)
        if status.game_over:
            await self.finish_game(game)
        else:
            await self.games.save(game)
        return text, status

    async def next_turn(self, game) -> tuple[str, ActionOutcome]:
        text = advance_day(game)
        await self.games.save(game)
        status = check_game_status(game)
        if status.game_over:
            await self.finish_game(game)
        else:
            await self.games.save(game)
        return text, status

    async def buy_upgrade(self, game, upgrade_id: int) -> str:
        upgrade = await self.upgrades.get_upgrade(upgrade_id)
        if upgrade is None:
            return "Улучшение не найдено."
        if upgrade.one_time and await self.upgrades.has_upgrade(game.id, upgrade_id):
            return "Это улучшение уже куплено."
        if game.money < upgrade.cost:
            return "Недостаточно денег для покупки."
        game.money -= upgrade.cost
        game.money += upgrade.money_bonus
        game.reputation += upgrade.reputation_bonus
        game.clients += upgrade.clients_bonus
        game.product_level += upgrade.product_bonus
        game.team_level += upgrade.team_bonus
        game.marketing_level += upgrade.marketing_bonus
        game.risk += upgrade.risk_bonus
        await self.games.save(game)
        await self.upgrades.grant_upgrade(game.id, upgrade_id)
        logger.info("Game %s purchased upgrade %s", game.id, upgrade.name)
        return f"🛍 Куплено улучшение: {upgrade.name}. {upgrade.description}"

    async def finish_game(self, game) -> None:
        score = calculate_score(game)
        result = GameResult(
            user_id=game.user_id,
            startup_name=game.startup_name,
            niche=game.startup_niche.value,
            final_day=game.current_day,
            final_money=game.money,
            final_reputation=game.reputation,
            final_clients=game.clients,
            score=score,
            outcome=game.game_status.value,
        )
        await self.games.save(game)
        await self.results.save_result(result)

    async def reset_game(self, user_id: int) -> None:
        await self.games.delete_active_game(user_id)

    async def leaderboard_text(self) -> str:
        results = await self.results.top_results(10)
        if not results:
            return "Лидерборд пока пуст. Сыграйте первую игру!"
        lines = ["🏅 *Топ стартапов*\n"]
        for index, result in enumerate(results, start=1):
            owner = result.user.username or result.user.full_name
            lines.append(
                f"{index}. {result.startup_name} — {result.score} очков | {owner} | клиенты: {result.final_clients}, деньги: {result.final_money:,} ₽"
            )
        return "\n".join(lines)
