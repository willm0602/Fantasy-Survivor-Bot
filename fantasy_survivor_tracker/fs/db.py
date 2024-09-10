"""
Connects to supabase
"""

from os import environ
from typing import List, Literal

import supabase
from discord.user import User

from . import constants as C
from ._types import BackupRow, Bet2, CommandRun, FantasyPlayer, Survivor


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

    def get_registed_user_id_or_false(self, user: User):
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

    def get_registed_user_or_false(self, user: User):
        """NOTE: this will be deprecated soon, should use `get_registered_user_id_or_false` instead"""
        return self.get_registered_user_id_or_false(user)
        
    def get_registed_user_by_id_or_false(
        self, id: int
    ) -> "Literal[False] | FantasyPlayer":
        """Returns the information for a user using their FP ID"""
        query = (
            self.supabase.from_(C.TABLE_NAMES.FANTASY_PLAYERS)
            .select("*")
            .filter("id", "eq", id)
            .execute()
            .data
        )
        if query:
            return query[0]
        return False

    def get_survivor_by_name_or_false(self, name) -> "Literal[False] | Survivor":
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
            .ilike("name", name)
            .execute()
            .data
        )
        if len(query):
            return query[0]
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
            .eq("id", id)
            .execute()
            .data
        )
        if len(query):
            return query[0]
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
        bets = self.supabase.from_(C.TABLE_NAMES.BET).select("*").execute().data
        user_bets = []
        for bet in bets:
            if bet.get("fantasyPlayer") == user_id:
                user_bets.append(bet)
        return user_bets

    def get_all_bets_for_user_by_discord_id(self, discord_id: str) -> List[Bet2]:
        """Gets all of the bets a user has given their discord id"""
        return (
            self.supabase.from_(C.TABLE_NAMES.BET)
            .select("*")
            .eq("discord_id", discord_id)
            .execute()
            .data
        )

    def get_bet_value(self, bet: Bet2) -> float:
        """
        NOTE: Should not be used, this is just being left in since there are some places when using
        an old betting system that use this
        returns the value of a bet

        bet: Bet
        returns: float
            returns the value

        This will throw a KeyError if the bet passed in isn't actually
        a bet
        """
        return bet["amount"]

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

    def get_all_fantasy_players(self) -> List[FantasyPlayer]:
        """
        returns: List[dict]
        """
        fps = self.supabase.from_("FantasyPlayers").select("*").execute().data
        return fps

    def get_all_bets(self) -> "List[Bet2]":
        bets = self.supabase.from_(C.TABLE_NAMES.BET).select("*").execute().data
        return bets

    # !commands for admins to interact with fantasy players

    def create_fantasy_player(self, user: User) -> None:
        """
        Adds a discord user to the database

        user: discord.user.User-
            the discord user that is being added to the db
        """
        name = user.display_name
        id = user.id
        self.player_table.insert(
            {"name": str(name), "bank": C.DEFAULT_BANK, "discord_id": id}
        ).execute()

    def del_fantasy_player(self, user: User):
        """
        Removes a discord user from the database

        user: discord.user.User-
            the discord user that is being removed from the db

        @returns None
        """
        player_id = self.get_registed_user_id_or_false(user)
        self.supabase.from_(C.TABLE_NAMES.BET).delete().match(
            {"fantasyPlayer": player_id}
        ).execute()

        self.supabase.from_("FantasyPlayers").delete().match(
            {"discord_id": str(user.id)}
        ).execute()

    def update_balance(self, user: User, new_bal: float = 0):
        """
        Updates a discord users bank from the database

        user: discord.user.User-
            the discord user that is being removed from the db

        @returns None
        """
        self.supabase.from_(C.TABLE_NAMES.FANTASY_PLAYERS).update(
            {"bank": new_bal}
        ).match({"discord_id": str(user.id)}).execute()

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
        Modifies all of the bets for a survivor to be multiplied by a factor

        name: str-
            the name of the survivor players

        factor: float-
            the factor to multiply the survivor players score by
        """
        survivor = self.get_survivor_by_name_or_false(name)
        bets = self.get_all_bets()

        for bet in bets:
            if bet["survivorPlayer"] == survivor["id"]:
                self.supabase.from_(C.TABLE_NAMES.BET).update(
                    {"amount": bet["amount"] * factor}
                ).eq("id", bet["id"]).execute()

    def delete_survivor_player(self, name: str):
        self.supabase.from_(C.TABLE_NAMES.BET).delete().neq("id", -1).execute()
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

        backup_data: List[BackupRow] = (
            self.supabase.from_(C.TABLE_NAMES.BACKUP).select("*").execute().data
        )
        for row in backup_data:
            self.supabase.table(row["tableName"]).insert(row["rowInfo"]).execute()

    def reset_season(self):
        self.supabase.from_(C.TABLE_NAMES.BET).delete().neq("id", 0).execute()
        self.supabase.from_(C.TABLE_NAMES.FANTASY_PLAYERS).delete().neq(
            "id", 0
        ).execute()
        self.supabase.from_(C.TABLE_NAMES.SURVIVOR_PLAYERS).delete().neq(
            "id", 0
        ).execute()

    def get_unspent_balance(self, id: int = None, discord_id: str = None) -> float:
        """
        gets the balance of a fantasy player

        id: int-
            the id of the fantasy player

        discord_int: str-
            the discord id for the fantasy player

        returns: float
            the users balance that is not spent on other players currently
        """

        sync_builder = self.supabase.from_("FantasyPlayers").select("*")
        if discord_id:
            query: List[FantasyPlayer] = (
                sync_builder.match({"discord_id": discord_id}).execute().data
            )
        else:
            query: List[FantasyPlayer] = sync_builder.match({"id": id}).execute().data
        if len(query):
            print("THERE IS A QUERY RESULT", query[0])
            return query[0].get("bank", 0)
        return None

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
            returns true if the bet is successfully made, otherwise False

        """
        print("CREATING BET", user, survivor, bet)
        if self.is_locked():
            raise Exception("Error: Betting is locked")
        fp_id = self.get_registed_user_id_or_false(user)
        if not fp_id:
            raise Exception("Error: you must be registered to place bets")
        prev_bal = self.get_unspent_balance(fp_id)
        survivor_name = survivor
        survivor = self.get_survivor_by_name_or_false(survivor)
        if not survivor:
            raise Exception(f"Survivor {survivor_name} does not exist")
        survivor_id = survivor.get("id")
        if prev_bal <= bet:
            bet = prev_bal
        print("\n\nAMOUNT", bet)
        self.supabase.table(C.TABLE_NAMES.BET).insert(
            {
                "fantasyPlayer": fp_id,
                "survivorPlayer": survivor_id,
                "amount": bet,
                "discord_id": user.id,
                "survivor_name": survivor,
            }
        ).execute()
        self.update_balance(user, prev_bal - bet)
        return True

    def remove_bet(self, survivor_name: str, user: User):
        """
        deletes the bet with the given id, then adds the balance to the FP's balance

        survivor_name: str
            the name of the survivor player that the user is removing all the bets for

        user: discord.User
            the discord user we are removing the bets for
        returns: None
        """
        if self.is_locked():
            raise Exception("Betting is locked")

        bets: Bet2 = (
            self.supabase.from_(C.TABLE_NAMES.BET)
            .select("*")
            .eq("discord_id", user.id)
            .execute()
            .data
        )

        survivor_id = self.get_survivor_by_name_or_false(survivor_name).get("id")
        user_id = self.get_registed_user_id_or_false(user)

        if not survivor_id:
            raise Exception(f"{survivor_name} is not a survivor")

        for bet in bets:
            if (
                bet.get("survivorPlayer") == survivor_id
                and bet.get("fantasyPlayer") == user_id
            ):
                old_bal = self.get_unspent_balance(user_id)
                new_bal = old_bal + bet.get("amount")
                self.update_balance(user, new_bal)
                betExists = True
        if not betExists:
            raise Exception("Error: bet does not exist")
        self.supabase.from_(C.TABLE_NAMES.BET).delete().match(
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
        user_id = self.get_registed_user_id_or_false(user)
        if user_id is False:
            raise Exception("Error: No user found for this user")
        total_bal = self.get_total_bal(discord_id=user.id)
        self.supabase.from_(C.TABLE_NAMES.BET).delete().eq(
            "discord_id", user.id
        ).execute()
        self.update_balance(user, total_bal)

    def get_total_bal(self, id: int = None, discord_id=None) -> float:
        """
        Get the total balance for a user
        """
        if id is None and discord_id is None:
            raise Exception("Error: must provide id or discord_id")

        if discord_id is not None:
            bets = self.get_all_bets_for_user_by_discord_id(discord_id)
            total = self.get_unspent_balance(discord_id=discord_id)
        else:
            bets = self.get_all_bets_for_user(id=id)
            total = self.get_unspent_balance(id=id)
        for bet in bets:
            total = total + self.get_bet_value(bet)
        return total

    #! Lets admins control settings
    def set_setting(self, key: str, val: str):
        setting_exists = (
            self.supabase.from_("Settings")
            .select("*")
            .match({"key": key})
            .execute()
            .data
        )
        if setting_exists:
            self.supabase.from_("Settings").update({"val": val}).match(
                {"key": key}
            ).execute()
        else:
            self.supabase.from_("Settings").insert({"key": key, "val": val}).execute()

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

    def log_command_to_db(self, command: "CommandRun") -> None:
        self.supabase.from_(C.TABLE_NAMES.COMMAND_RUN_TABLE).insert(command).execute()

    def deduct_unspent_points_by_five_percent(self) -> None:
        """Deducts all unspent points by users by five-percent"""
        updated_player_info = []
        for player in self.get_all_fantasy_players():
            bank = player["bank"] * 0.95
            updated_player_info.append({"id": player["id"], "bank": bank})
        self.supabase.from_(C.TABLE_NAMES.FANTASY_PLAYERS).upsert(
            updated_player_info
        ).execute()

    def get_all_settings(self) -> dict:
        """Returns a dictionary of all the settings and their values"""
        settings = (
            self.supabase.from_(C.TABLE_NAMES.SETTINGS).select("*").execute().data
        )
        settings_dict = {}
        for setting in settings:
            key = setting["key"]
            val = setting["val"]
            settings_dict[key] = val
        return settings_dict

    def get_all_errors(self) -> List[CommandRun]:
        """Returns all Command Runs with errors"""
        command_runs: List[CommandRun] = (
            self.supabase.from_(C.TABLE_NAMES.COMMAND_RUN_TABLE)
            .select("*")
            .match({"errored": True})
            .order("id", desc=True)
            .execute()
            .data
        )
        return command_runs

    def get_error_by_id(self, id: int) -> CommandRun | None:
        """Returns the command run for the error with the given id"""
        errors = self.get_all_errors()
        for error in errors:
            if error["id"] == id:
                return error
        return None
