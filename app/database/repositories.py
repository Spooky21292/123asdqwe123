from __future__ import annotations

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Game, GameResult, Upgrade, User, UserUpgrade
from app.models.enums import GameStatus


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_or_create_user(self, telegram_id: int, username: str | None, full_name: str) -> User:
        result = await self.session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        if user:
            user.username = username
            user.full_name = full_name
            await self.session.commit()
            await self.session.refresh(user)
            return user
        user = User(telegram_id=telegram_id, username=username, full_name=full_name)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def count_users(self) -> int:
        result = await self.session.execute(select(func.count(User.id)))
        return int(result.scalar_one())

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self.session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()


class GameRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_active_game(self, user_id: int) -> Game | None:
        result = await self.session.execute(
            select(Game)
            .options(selectinload(Game.user_upgrades).selectinload(UserUpgrade.upgrade))
            .where(Game.user_id == user_id)
            .where(Game.game_status == GameStatus.ACTIVE)
        )
        return result.scalar_one_or_none()

    async def create_game(self, user_id: int, startup_name: str, startup_niche: str, **stats: int) -> Game:
        await self.session.execute(delete(Game).where(Game.user_id == user_id, Game.game_status == GameStatus.ACTIVE))
        game = Game(user_id=user_id, startup_name=startup_name, startup_niche=startup_niche, **stats)
        self.session.add(game)
        await self.session.commit()
        await self.session.refresh(game)
        return game

    async def save(self, game: Game) -> Game:
        self.session.add(game)
        await self.session.commit()
        await self.session.refresh(game)
        return game

    async def delete_active_game(self, user_id: int) -> None:
        await self.session.execute(delete(Game).where(Game.user_id == user_id, Game.game_status == GameStatus.ACTIVE))
        await self.session.commit()

    async def count_active_games(self) -> int:
        result = await self.session.execute(select(func.count(Game.id)).where(Game.game_status == GameStatus.ACTIVE))
        return int(result.scalar_one())

    async def get_game_by_id(self, game_id: int) -> Game | None:
        result = await self.session.execute(select(Game).where(Game.id == game_id))
        return result.scalar_one_or_none()


class UpgradeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_upgrades(self) -> list[Upgrade]:
        result = await self.session.execute(select(Upgrade).order_by(Upgrade.cost.asc()))
        return list(result.scalars().all())

    async def has_upgrade(self, game_id: int, upgrade_id: int) -> bool:
        result = await self.session.execute(
            select(UserUpgrade).where(UserUpgrade.game_id == game_id, UserUpgrade.upgrade_id == upgrade_id)
        )
        return result.scalar_one_or_none() is not None

    async def grant_upgrade(self, game_id: int, upgrade_id: int) -> None:
        self.session.add(UserUpgrade(game_id=game_id, upgrade_id=upgrade_id))
        await self.session.commit()

    async def get_upgrade(self, upgrade_id: int) -> Upgrade | None:
        result = await self.session.execute(select(Upgrade).where(Upgrade.id == upgrade_id))
        return result.scalar_one_or_none()


class ResultRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_result(self, result_obj: GameResult) -> None:
        self.session.add(result_obj)
        await self.session.commit()

    async def top_results(self, limit: int = 10) -> list[GameResult]:
        result = await self.session.execute(
            select(GameResult).options(selectinload(GameResult.user)).order_by(GameResult.score.desc()).limit(limit)
        )
        return list(result.scalars().all())
