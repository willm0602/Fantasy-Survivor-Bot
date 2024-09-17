"""
lets a user view their bets

fs.list_bets [?@user]
"""

from ...command import UserCommand
from ..utils import list_bets

LIST_BETS_COMMAND = UserCommand(
    "list_bets",
    list_bets,
    "fs.list_bets [?@user] - lets a user view the bets of a user or defaults to themselves",
)
