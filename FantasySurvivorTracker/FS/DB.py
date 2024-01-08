"""
Connects to supabase
"""

import json
from os import environ
from typing import List, Literal

import supabase
from discord.user import User

from . import Constants as C
from .Types import Bet, Bet2, CommandRun, FantasyPlayer, Survivor

# default bank value that a user has when starting
# TODO: move to setting when it is ready
DEFAULT_BANK = 1000


class DB:
    """
    Constructor- loads information from the config.json file to
    connect to supabase
    """
    supabase: supabase.Client

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
            .ilike('name', name)
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
            .eq('id', id)
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
        bets = self.supabase.from_("Bet").select("*").execute().data
        user_bets = []
        for bet in bets:
            if bet.get("fantasyPlayer") == user_id:
                user_bets.append(bet)
        return user_bets

    
    def get_all_bets_for_user_by_discord_id(self, discord_id: str) -> List[Bet2]:
        """Gets all of the bets a user has given their discord id"""
        return self.supabase.from_(
            C.TABLE_NAMES.BET
        ).select("*").eq(
            'discord_id', discord_id
        ).execute().data
    
    def get_bet_value(self, bet: dict) -> float:
        """
        DEPRECATED
        returns the value of a bet

        bet: Bet
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

    def get_all_bets(self) -> 'List[Bet2]':
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
        Modifies all of the bets for a survivor to be multiplied by a factor

        name: str-
            the name of the survivor players

        factor: float-
            the factor to multiply the survivor players score by
        """
        bets_table = C.TABLE_NAMES.BET
        query = f'UPDATE {bets_table} SET amount = amount * 2'
        self.supabase.execute(query)

    def delete_survivor_player(self, name: str):
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
        self.supabase.from_(C.TABLE_NAMES.BET).delete().neq("id", 0).execute()
        self.supabase.from_(C.TABLE_NAMES.FANTASY_PLAYERS).delete().neq("id", 0).execute()
        self.supabase.from_(C.TABLE_NAMES.SURVIVOR_PLAYERS).delete().neq("id", 0).execute()

    def get_unspent_balance(self, id: int=None, discord_id: str = None) -> FantasyPlayer:
        """
        gets the balance of a fantasy player

        id: int-
            the id of the fantasy player
            
        discord_int: str-
            the discord id for the fantasy player

        returns: float
            the users balance that is not spent on other players currently
        """

        if discord_id:
            query: List[FantasyPlayer] = self.supabase.from_("FantasyPlayers").eq('discord_id', discord_id).select("*").execute().data
        else:            
            query: List[FantasyPlayer] = self.supabase.from_("FantasyPlayers").select("*").execute().data
        if len(query):
            return query[0]['bank']
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
        fp_id = self.get_registed_user_or_false(user)
        if not fp_id:
            raise Exception('Error: you must be registered to place bets')
        prev_bal = self.get_unspent_balance(fp_id)
        survivor_name = survivor
        survivor = self.get_survivor_by_name_or_false(survivor)
        if not survivor:
            raise Exception(f"Survivor {survivor_name} does not exist")
        survivor_id = survivor.get("id")
        if prev_bal >= bet:
            bet = prev_bal
        self.supabase.table(C.TABLE_NAMES.BET).insert(
            {
                "fantasyPlayer": fp_id,
                "survivorPlayer": survivor_id,
                "amount": bet,
                'discord_id': user.id,
                'survivor_name': survivor
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
        
        bets: Bet2 = self.supabase.from_(
            C.TABLE_NAMES.BET
        ).select("*").eq('discord_id', user.id).execute().data
        
        survivor_id = self.get_survivor_by_name_or_false(survivor_name).get("id")
        user_id = self.get_registed_user_or_false(user)
        
        if not survivor_id:
            raise Exception(f"{survivor_name} is not a survivor")
        
        for bet in bets:
            if (
                bet.get("survivorPlayer") == survivor_id
                and bet.get("fantasyPlayer") == user_id
            ):
                old_bal = self.get_unspent_balance(user_id)
                new_bal = old_bal + bet.get('amount')
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
        self.update_balance(user)
        self.supabase.from_(C.TABLE_NAMES.BET).delete().eq('discord_id', user.id).execute()
    
    def get_total_bal(self, id: int) -> float:
        """
        Get the total balance for a user
        """
        bets = self.get_all_bets_for_user(id)
        total = self.get_unspent_balance(id)
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
