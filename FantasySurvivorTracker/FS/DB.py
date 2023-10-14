"""
Connects to supabase
"""

import json
from os import environ
from typing import List, Literal

import supabase
from discord.user import User

from . import Constants as C
from .Types import Bet, CommandRun, FantasyPlayer, Survivor

# default bank value that a user has when starting
# TODO: move to setting when it is ready
DEFAULT_BANK = 1000


class DB:
    """
    Constructor- loads information from the config.json file to
    connect to supabase
    """

    def __init__(self):
        supabase_url = environ["supabase_url"]
        supabase_key = environ["supabase_key"]
        self.supabase: supabase.Client = supabase.create_client(
            supabase_url, supabase_key
        )
        self.player_table = self.supabase.table(C.TABLE_NAMES.FANTASY_PLAYERS)

    # !helper commands

    def get_registed_user_or_false(self, user: User):
        """
        Check's if there is a fantasy player cooresponding to the discord user

        user: discord.user.User-
            the discord user that is being checked

        @returns bool | int : returns the id of the discord user if they exist,
            otherwise returns false
        """
        query = (
            self.supabase.from_(C.TABLE_NAMES.FANTASY_PLAYERS)
            .select("*")
            .execute()
            .data
        )
        for _user in query:
            if _user.get("discord_id") == str(user.id):
                return _user.get("id")
        return False

    def get_registed_user_by_id_or_false(
        self,
        id: int
    ) -> 'Literal[False] | FantasyPlayer':
        """Returns the information for a user using their FP ID"""
        query = (
            self.supabase.from_(C.TABLE_NAMES.FANTASY_PLAYERS)
            .select("*")
            .filter('id', 'eq', id)
            .execute()
            .data
        )
        if query:
            return query[0]
        return False

    def get_survivor_by_name_or_false(
        self,
        name
    ) -> 'Literal[False] | Survivor':
        """
        Check's if there is a Survivor player with the given name

        name: str-
            The name being checked to see if there is a survivor player affiliated with them
            in the name

        @returns dict:
            id: int
                id of user in db
            created_at: date
                the date the user was created
            name: str
                the name of the fantasy player
            balance: float
                the score a fantasy player currently has
        """
        query = (
            self.supabase.from_(C.TABLE_NAMES.SURVIVOR_PLAYERS)
            .select("*")
            .execute()
            .data
        )
        for _user in query:
            if _user.get("name").lower().strip() == name.lower().strip():
                return _user
        return False

    def get_survivor_player_by_id_or_false(self, id):
        """
        Check's if there is a Survivor player with the given id

        id: int-
            The name being checked to see if there is a survivor player
            with that id

        @returns false | dict:
            id: int
                id of user in db
            created_at: date
                the date the user was created
            name: str
                the name of the fantasy player
            balance: float
                the score a fantasy player currently has
        """
        query = (
            self.supabase.from_(C.TABLE_NAMES.SURVIVOR_PLAYERS)
            .select("*")
            .execute()
            .data
        )
        for _user in query:
            if _user.get("id") == id:
                return _user
        return False

    def get_all_bets_for_user(self, id: int):
        """
        gets all the bets a user has

        id: int
            the id of the user in the db

        returns: List[dict]
            id: int
                the id of the bet
            survivorPlayer: int
                the id of the survivor player in the db
            fantasyPlayer: int
                the id of the fantasy player in the db
            amount: float
                the amount the bet is for
        """
        user_id = id
        bets = self.supabase.from_("Bet").select("*").execute().data
        user_bets = []
        for bet in bets:
            if bet.get("fantasyPlayer") == user_id:
                user_bets.append(bet)
        return user_bets

    def get_bet_value(self, bet: dict) -> float:
        """
        returns the value of a bet

        bet: dict
            id: int
                the id of the bet
            fantasyPlayer: int
                the id of the fantasy player that made the bet
            survivorPlayer: int
                the id of the survivor player the bet is on
            amount: float
                the "number of shares" of a survivor player made by the bet

        returns: float
            returns the value
        """
        share_count = bet.get("amount", None)
        if share_count is None:
            raise Exception("Unable to get value from bet, please check logs")
        survivor = self.get_survivor_player_by_id_or_false(bet.get("survivorPlayer"))
        bal = survivor.get("balance")
        return bal * share_count

    def get_all_survivors(self) -> List[Survivor]:
        """
        gets a list of all survivors

        returns: List[dict]
            id: int
                id of user in db
            created_at: date
                the date the user was created
            name: str
                the name of the fantasy player
            balance: float
                the score a fantasy player currently has
        """
        survivors = (
            self.supabase.from_(C.TABLE_NAMES.SURVIVOR_PLAYERS)
            .select("*")
            .execute()
            .data
        )
        return survivors

    def get_all_fantasy_players(self):
        """
        returns: List[dict]
        """
        fps = self.supabase.from_("FantasyPlayers").select("*").execute().data
        return fps

    def get_all_bets(self) -> 'List[Bet]':
        bets = self.supabase.from_("Bet").select("*").execute().data
        return bets

    # !commands for admins to interact with fantasy players

    def create_fantasy_player(self, user: User):
        """
        Adds a discord user to the database

        user: discord.user.User-
            the discord user that is being added to the db

        @returns None
        """
        name = user.display_name
        id = user.id
        self.player_table.insert(
            {"name": str(name), "bank": DEFAULT_BANK, "discord_id": id}
        ).execute()

    def del_fantasy_player(self, user: User):
        """
        Removes a discord user from the database

        user: discord.user.User-
            the discord user that is being removed from the db

        @returns None
        """
        player_id = self.get_registed_user_or_false(user)
        self.supabase.from_("Bet").delete().match(
            {"fantasyPlayer": player_id}
        ).execute()

        self.supabase.from_("FantasyPlayers").delete().match(
            {"discord_id": str(user.id)}
        ).execute()

    def update_balance(self, user: User, new_bal: float = 0):
        """
        Removes a discord user from the database

        user: discord.user.User-
            the discord user that is being removed from the db

        @returns None
        """
        self.supabase.from_("FantasyPlayers").update({"bank": new_bal}).match(
            {"discord_id": str(user.id)}
        ).execute()

    # !commands for admins to interact with survivor players

    def create_survivor_player(self, name: str):
        """
        Creates a new Survivor Player in the database

        name: str
            the name of the survivor player (NOTE: MUST BE ONE WORD)

        returns: None
        """
        self.supabase.table(C.TABLE_NAMES.SURVIVOR_PLAYERS).insert(
            {"name": name}
        ).execute()

    def update_survivor_player(self, name: str, factor: float):
        """
        Multiplies a survivor players score by the given factor
        e.g. if player has a score of 2, passing in their name
        and 1.3 will let them have a score of 2.6.

        name: str-
            the name of the survivor players

        factor: float-
            the factor to multiply the survivor players score by
        """
        survivor_players = (
            self.supabase.from_(C.TABLE_NAMES.SURVIVOR_PLAYERS)
            .select("*")
            .execute()
            .data
        )
        for player in survivor_players:
            if player.get("name") == name:
                bal = player.get("balance", 0)
                factor = float(factor)
                bal = bal * factor
                self.supabase.from_(C.TABLE_NAMES.SURVIVOR_PLAYERS).update(
                    {"balance": bal}
                ).match({"name": name}).execute()
                return

    def delete_survivor_player(self, name: str):
        survivor_player = self.get_survivor_by_name_or_false(name)["id"]
        self.supabase.from_("Bet").delete().match(
            {"survivorPlayer": survivor_player}
        ).execute()
        if self.get_survivor_by_name_or_false(name):
            self.supabase.from_(C.TABLE_NAMES.SURVIVOR_PLAYERS).delete().match(
                {"name": name}
            ).execute()

    def backup(self):
        # deletes previous backup
        self.supabase.from_(C.TABLE_NAMES.BACKUP).delete().neq("id", 0).execute()

        # backs up survivor scores
        survivors = self.get_all_survivors()
        for survivor in survivors:
            self.supabase.table(C.TABLE_NAMES.BACKUP).insert(
                {
                    "id": survivor["id"],
                    "tableName": C.TABLE_NAMES.SURVIVOR_PLAYERS,
                    "rowInfo": survivor,
                }
            ).execute()

        # backs up fantasy player data
        fantasy_players = self.get_all_fantasy_players()
        for fp in fantasy_players:
            self.supabase.table(C.TABLE_NAMES.BACKUP).insert(
                {
                    "id": fp["id"],
                    "tableName": C.TABLE_NAMES.FANTASY_PLAYERS,
                    "rowInfo": fp,
                }
            ).execute()

        # backs up bets placed
        bets = self.get_all_bets()
        for bet in bets:
            self.supabase.table(C.TABLE_NAMES.BACKUP).insert(
                {"id": bet["id"], "tableName": C.TABLE_NAMES.BET, "rowInfo": bet}
            ).execute()

    def restore(self):
        # clears all data not backed up
        self.reset_season()

        backup_data = (
            self.supabase.from_(C.TABLE_NAMES.BACKUP).select("*").execute().data
        )
        for row in backup_data:
            self.supabase.table(row.get("tableName")).insert(
                row.get("rowInfo")
            ).execute()

    def reset_season(self):
        self.supabase.from_("Bet").delete().neq("id", 0).execute()
        self.supabase.from_("FantasyPlayers").delete().neq("id", 0).execute()
        self.supabase.from_(C.TABLE_NAMES.SURVIVOR_PLAYERS).delete().neq("id", 0).neq(
            "id", 0
        ).execute()

    # !Commands for Users

    def get_balance(self, id: int):
        """
        gets the balance of a fantasy player

        id: int-
            the id of the fantasy player

        returns: float
            the users balance that is not spent on other players currently
        """

        query = self.supabase.from_("FantasyPlayers").select("*").execute().data
        for _user in query:
            if _user.get("id") == id:
                return _user.get("bank", False)
        return False

    def create_bet(self, user: User, survivor: str, bet: float):
        """
        creates a bet for the user

        user: discord.user.User-
            user that is making the bet
        survivor: string-
            name of the survivor
        bet: float-
            the amount being bet

        returns: bool
            returns true if the bet is succesfully made, otherwise False

        """
        if self.is_locked():
            raise Exception("Error: Betting is locked")
        id = self.get_registed_user_or_false(user)
        prev_bal = self.get_balance(id)
        survivor_name = survivor
        survivor = self.get_survivor_by_name_or_false(survivor)
        if not survivor:
            raise Exception(f"Survivor {survivor_name} does not exist")
        survivor_id = survivor.get("id")
        if prev_bal >= bet:
            bet = bet / survivor.get("balance")
        elif prev_bal > 0:
            bet = prev_bal / survivor.get("balance")
        else:
            raise Exception("Invalid Bet Amount")
        user_id = self.get_registed_user_or_false(user)
        if user_id and survivor_id:
            self.supabase.table("Bet").insert(
                {
                    "fantasyPlayer": user_id,
                    "survivorPlayer": survivor_id,
                    "amount": bet,
                }
            ).execute()
            self.update_balance(user, prev_bal - bet * survivor.get("balance"))
            return True
        if user_id:
            raise Exception("Invalid Survivor")
        else:
            raise Exception("Invalid: I don't believe you are playing")


    def remove_bet(self, survivor_name: str, user: User):
        """
        deletes the bet with the given id, then adds the balance to the FP's balance

        survivor_name: str
            the name of the survivor player that the user is removing all the bets for
        returns: None
        """
        if self.is_locked():
            raise Exception("Betting is locked")
        bets = self.supabase.from_("Bet").select("*").execute().data
        betExists = False
        survivor_id = self.get_survivor_by_name_or_false(survivor_name).get("id")
        user_id = self.get_registed_user_or_false(user)
        if not survivor_id:
            raise Exception(f"{survivor_name} is not a survivor")
        for bet in bets:
            if (
                bet.get("survivorPlayer") == survivor_id
                and bet.get("fantasyPlayer") == user_id
            ):
                old_bal = self.get_balance(user_id)
                new_bal = old_bal + self.get_bet_value(bet)
                self.update_balance(user, new_bal)
                betExists = True
        if not betExists:
            raise Exception("Error: bet does not exist")
        self.supabase.from_("Bet").delete().match(
            {"fantasyPlayer": user_id, "survivorPlayer": survivor_id}
        ).execute()

    def remove_all_bets(self, user: User):
        """
        removes all bets a user has

        user: discord.user.User
            the user to remove all the bets for

        returns: None
        """
        if self.is_locked():
            raise Exception("Betting is locked")
        user_id = self.get_registed_user_or_false(user)
        if user_id is False:
            raise Exception("Error: No user found for this user")
        bets = self.get_all_bets_for_user(user_id)
        for bet in bets:
            survivor_id = bet.get('survivorPlayer')
            survivor = self.get_survivor_player_by_id_or_false(survivor_id)['name']
            self.remove_bet(survivor, user)

    def get_total_bal(self, id: int):
        """ """
        bets = self.get_all_bets_for_user(id)
        total = self.get_balance(id)
        for bet in bets:
            total = total + self.get_bet_value(bet)
        return total

    #! Lets admins control settings
    def set_setting(self, key: str, val: str):
        setting_exists = self.supabase.from_('Settings').select('*').match({
            'key': key
        }).execute().data
        if setting_exists:
            self.supabase.from_("Settings").update({"val": val}).match(
                {"key": key}
            ).execute()
        else:
            self.supabase.from_('Settings').insert({'key': key, 'val': val}).execute()

    def get_setting(self, key):
        query = self.supabase.from_("Settings").select("*").execute().data
        for setting in query:
            if setting.get("key") == key:
                return setting.get("val")
        return None

    def lock_bets(self):
        self.set_setting("bettingLocked", "yes")

    def unlock_bets(self):
        self.set_setting("bettingLocked", "no")

    def is_locked(self):
        return self.get_setting("bettingLocked") == "yes"

    def log_command_to_db(self, command: 'CommandRun') -> None:
        print('COMMAND IS', command)
        self.supabase.from_(C.TABLE_NAMES.COMMAND_RUN_TABLE).insert(command).execute()
