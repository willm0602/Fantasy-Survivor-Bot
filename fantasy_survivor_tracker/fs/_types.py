from datetime import datetime
from typing import List, TypedDict


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


class Bet2(TypedDict):
    """Updated version of Bet to include fantasy players
    discord id for faster querying"""

    id: int
    created_at: datetime
    amount: float
    fantasyPlayer: int
    survivorPlayer: int
    survivor_name: str
    discord_id: str


class CommandRun(TypedDict):
    id: int
    time_ran: datetime
    user_ran: str
    time_to_complete: float
    errored: bool
    trigger: str
    arguments: List[str]
    traceback: str


class Setting(TypedDict):
    key: str
    val: str


class BackupRow(TypedDict):
    identifier: int
    tableName: str
    rowInfo: str


class SurvivorAlias(TypedDict):
    id: int
    created_at: datetime
    alias: str
    survivor_id: int