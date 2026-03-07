from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        query = select(User).where(User.telegram_id == telegram_id)
        return await self.session.scalar(query)

    async def get_or_create(self, telegram_id: int, username: str | None, first_name: str | None) -> User:
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            user.username = username
            user.first_name = first_name
            await self.session.commit()
            return user

        user = User(telegram_id=telegram_id, username=username, first_name=first_name)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_settings(self, user: User, timezone: str | None = None, reminders_enabled: bool | None = None) -> User:
        if timezone is not None:
            user.timezone = timezone
        if reminders_enabled is not None:
            user.reminders_enabled = reminders_enabled
        await self.session.commit()
        await self.session.refresh(user)
        return user
