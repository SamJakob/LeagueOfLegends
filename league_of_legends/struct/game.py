from typing import Optional

from .. import struct as _struct


class Game:
    """
    Represents a game of League of Legends.
    """

    def __init__(self, initial_events: list[_struct.GameEvent], players: list[_struct.GamePlayer]):
        self.events = initial_events
        self.players = players

    def has_active_player(self) -> bool:
        """
        Whether there exists an active player in this game.
        :return: True if there is an active player, False if there isn't or there are no players.
        """
        return len(self.players) > 0 and self.players[0].is_active_player is not None

    def get_active_player(self) -> Optional[_struct.GamePlayer]:
        """
        Returns the active player, if it exists.
        :return: The active GamePlayer if it exists, otherwise None.
        """
        for player in self.players:
            if player.is_active_player:
                return player

        return None

    def get_active_player_summoner(self) -> Optional[str]:
        """
        Returns the summoner name of the active player, if the active player exists.
        :return: The name as a string if the active player exists, otherwise None.
        """
        active_player = self.get_active_player()
        return active_player.summoner if active_player is not None else None

    def get_active_player_allies(self):
        """
        Returns the list of allies (players on the active player's team), if the active player exists.
        Otherwise, this returns None.
        :return: A list of GamePlayers who are the active player's allies if the active player
        exists, otherwise None.
        """
        active_player = self.get_active_player()

        if active_player is None:
            return None

        allies = []
        for player in self.players:
            if player.team == active_player.team:
                allies.append(player)

        return allies

    def get_active_player_enemies(self):
        """
        Returns the list of enemies (players not on the active player's team), if the active player
        exists. Otherwise, this returns None.
        :return: A list of GamePlayers who are the active player's enemies if the active player
        exists, otherwise None.
        """
        active_player = self.get_active_player()

        if active_player is None:
            return None

        enemies = []
        for player in self.players:
            if player.team != active_player.team:
                enemies.append(player)

        return enemies

    active_player = property(get_active_player)
    active_player_summoner = property(get_active_player_summoner)
    active_player_allies = property(get_active_player_allies)
    active_player_enemies = property(get_active_player_enemies)
