from datetime import datetime
from typing import TypedDict

class FantasyPlayer(TypedDict):
    id: int
    name: str
    discord_id: str
    bank: float

class Survivor(TypedDict):
    id: int
    name: str
    balance: float

class Bet(TypedDict):
    id: int
    created_at: datetime
    amount: float
    fantasyPlayer: int
    survivorPlayer: int