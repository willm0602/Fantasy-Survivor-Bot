"""
lets a user view their bets

fs.list_bets [?@user]
"""

from discord.message import Message

from ...Command import User_Command
from ...DB import DB
from ..utils import list_bets


LIST_BETS_COMMAND = User_Command(
    "list_bets",
    list_bets,
    "fs.list_bets [?@user] - lets a user view the bets of a user or defaults to themselves",
)
