from __future__ import annotations

from sqlalchemy import select

from app.database.base import Base
from app.database.session import AsyncSessionLocal, engine
from app.models import Upgrade

UPGRADES = [
    {"name": "Новый офис", "description": "Повышает командный дух и репутацию.", "cost": 18000, "team_bonus": 1, "reputation_bonus": 4, "one_time": True},
    {"name": "CRM-система", "description": "Автоматизирует работу с клиентами.", "cost": 14000, "clients_bonus": 25, "marketing_bonus": 1, "one_time": True},
    {"name": "Наставник", "description": "Снижает риск и помогает стратегии.", "cost": 22000, "reputation_bonus": 6, "risk_bonus": -8, "one_time": True},
    {"name": "Платная аналитика", "description": "Даёт более точные решения для продукта.", "cost": 16000, "product_bonus": 1, "marketing_bonus": 1, "one_time": True},
    {"name": "Дизайнер интерфейса", "description": "Повышает качество продукта.", "cost": 20000, "product_bonus": 2, "reputation_bonus": 3, "one_time": True},
    {"name": "Продакт-менеджер", "description": "Улучшает развитие продукта и команды.", "cost": 26000, "product_bonus": 1, "team_bonus": 1, "risk_bonus": -5, "one_time": True},
    {"name": "Рекламный пакет", "description": "Даёт постоянный бонус к маркетингу.", "cost": 24000, "marketing_bonus": 2, "clients_bonus": 40, "one_time": True},
    {"name": "Автоматизация процессов", "description": "Снижает расходы и риск.", "cost": 30000, "money_bonus": 8000, "team_bonus": 1, "risk_bonus": -10, "one_time": True},
]


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        existing = await session.execute(select(Upgrade))
        if existing.scalars().first() is None:
            for data in UPGRADES:
                session.add(Upgrade(**data))
            await session.commit()
