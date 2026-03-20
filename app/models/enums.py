from __future__ import annotations

from enum import Enum


class StartupNiche(str, Enum):
    EDTECH = "EdTech"
    FOODTECH = "FoodTech"
    ECOTECH = "EcoTech"
    GAMEDEV = "GameDev"
    FINTECH = "FinTech"


class GameStatus(str, Enum):
    NOT_STARTED = "not_started"
    ACTIVE = "active"
    WON = "won"
    LOST = "lost"
