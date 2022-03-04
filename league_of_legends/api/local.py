# League of Legends - Local (Live) Client Data API

import socket
import time
from typing import Tuple, Callable, Any

import requests

from league_of_legends import errors
from league_of_legends.struct import *
from .routing import LOCAL

# Disable HTTPS warnings from requests.
import requests.packages.urllib3 as urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def wait_for_local_game(on_poll: Callable[[float], Any]) -> Tuple[Game, float]:
    """
    Waits for the local user to start a game.
    This simply polls the local client API until a response is received that suggests a game has started or is in
    progress.
    :return: (Game, Wait Time; the amount of time waited before the game was found)
    """
    game = None
    waiting_start_time = time.time()

    try:
        while game is None:
            try:
                # Fetch the list of events.
                # If this fails with an exception, we know that the game cannot
                # have started yet, because the League of Legends client has not
                # yet made the API available.
                events = get_local_game_events()

                # Check if events contains a 'GameStart' event.
                for event in events:
                    if event.name == 'GameStart':
                        # If a GameStart event was found, the game has
                        # started, so let's create and return a Game object
                        # representing this game.
                        active_player = get_local_active_player()

                        game = Game(
                            initial_events=events,
                            players=get_local_game_players(active_player=active_player)
                        )
                        break
            except errors.ClientConnectError:
                on_poll(time.time() - waiting_start_time)
                time.sleep(0.05)
                continue
    except KeyboardInterrupt:
        print('\nInterrupted. Halting...')
        exit(0)

        # noinspection PyTypeChecker
        return None, None

    return game, time.time() - waiting_start_time


def get_local_game_events(skip_connection_test=False) -> list[GameEvent]:
    """
    Fetches the list of events that have occurred in the game from the League of Legends Live Client Data API.
    The JSON data is parsed and converted into a list of GameEvent classes.
    :param skip_connection_test: If set to true, the connection to the client API is not checked.
    :return: A list of GameEvents.
    """
    if not skip_connection_test:
        _test_connection(should_throw=True)

    response = requests.get(f'https://{LOCAL}/liveclientdata/eventdata', verify=False)
    data = response.json()

    if data is None or data.get('Events') is None:
        return []

    events = []
    for event in data.get('Events'):
        events.append(GameEvent(event))
    return events


def get_local_game_players(active_player: GameActivePlayer = None, skip_connection_test=False)\
        -> list[GamePlayer]:
    """
    Fetches the list of players that have occurred in the game from the League of Legends Live Client Data API.
    The JSON data is parsed and converted into a list of GamePlayer classes.
    :param active_player: If specified, additional data will be retrieved and inserted into whichever player
    is the active player from the active player data.
    :param skip_connection_test: If set to true, the connection to the client API is not checked.
    :return: A list of GamePlayers.
    """
    if not skip_connection_test:
        _test_connection(should_throw=True)

    response = requests.get(f'https://{LOCAL}/liveclientdata/playerlist', verify=False)
    data = response.json()

    if data is None or len(data) == 0:
        return []

    players = []
    for player in data:
        players.append(GamePlayer(player, active_player=active_player))
    return players


def get_local_active_player(skip_connection_test=False) -> GameActivePlayer:
    """
    Fetches the information about the currently active player on the local client from the League of Legends
    Live Client Data API.
    The JSON data is parsed and converted into a GameActivePlayer tuple.
    :param skip_connection_test: If set to true, the connection to the client API is not checked.
    :return: A GameActivePlayer tuple.
    """
    if not skip_connection_test:
        _test_connection(should_throw=True)

    response = requests.get(f'https://{LOCAL}/liveclientdata/activeplayer', verify=False)
    data = response.json()

    return GameActivePlayer(
        name=data['summonerName'],
        gold=data['currentGold'],
        champion_stats=data['championStats'],
        abilities=GameActivePlayerAbilities(
            q=data['abilities'].get('Q'),
            w=data['abilities'].get('W'),
            e=data['abilities'].get('E'),
            r=data['abilities'].get('R'),
            passive=data['abilities'].get('Passive')
        )
    )


def _test_connection(should_throw=False) -> bool:
    """
    Internal helper method to check if a connection can be made to the client
    API.
    :param should_throw: Whether an exception should be thrown, instead of just
    returning a Boolean. Useful when this is included in other methods as a
    guard.
    :return: True if a connection could be made, false if it couldn't and
    should_throw is false (per the default setting).
    """

    try:
        # Parse the address, and initialize a socket.
        address = LOCAL.split(':')
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Attempt to make a connection, then immediately close.
        # (2 is the shutdown reason.)
        connection.connect((address[0], int(address[1])))
        connection.shutdown(2)

        # If we did all above successfully, we may return True.
        return True
    except ConnectionRefusedError:
        # Otherwise, we encountered an exception, which we should
        # deal with accordingly.
        if should_throw:
            raise errors.ClientConnectError(LOCAL)
        else:
            return False
