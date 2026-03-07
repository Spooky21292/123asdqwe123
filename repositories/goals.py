from datetime import datetime

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Goal


class GoalRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user_id: int, title: str, description: str | None) -> Goal:
        goal = Goal(user_id=user_id, title=title, description=description)
        self.session.add(goal)
        await self.session.commit()
        await self.session.refresh(goal)
        return goal

    async def get_user_goals(self, user_id: int) -> list[Goal]:
        result = await self.session.scalars(select(Goal).where(Goal.user_id == user_id).order_by(Goal.created_at.desc()))
        return list(result)

    async def get_by_id(self, goal_id: int, user_id: int) -> Goal | None:
        return await self.session.scalar(select(Goal).where(and_(Goal.id == goal_id, Goal.user_id == user_id)))

    async def complete(self, goal: Goal) -> Goal:
        goal.is_completed = True
        goal.completed_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(goal)
        return goal

    async def delete(self, goal: Goal) -> None:
        await self.session.delete(goal)
        await self.session.commit()
