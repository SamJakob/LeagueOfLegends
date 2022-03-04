from collections import namedtuple

GamePlayerScores = namedtuple(
    'GamePlayerScores',
    ['assists', 'creep_score', 'deaths', 'kills', 'ward_score']
)

GamePlayerItem = namedtuple(
    'GamePlayerItem',
    ['id', 'name', 'slot', 'can_use', 'consumable', 'count', 'price']
)

GamePlayerRunes = namedtuple(
    'GamePlayerRunes',
    ['keystone', 'primary_tree', 'secondary_tree']
)

GameActivePlayerAbilities = namedtuple(
    'GameActivePlayerAbilities',
    ['q', 'w', 'e', 'r', 'passive']
)

GameActivePlayer = namedtuple(
    'GameActivePlayer',
    ['name', 'gold', 'champion_stats', 'abilities']
)


class GamePlayer:
    """
    Represents a player in a League of Legends game, as defined by the League
    of Legends client API.
    """

    def __init__(self, data, active_player: GameActivePlayer = None):
        """
        Initializes a GamePlayer (class to represent a player in League of Legends).
        :param data: The JSON data from the client API for the player.
        :param active_player: If specified, this is used to add additional properties
        if this class represents the active player.
        """

        if data.get('summonerName'):
            self.summoner = data['summonerName']

        self.team = data['team']
        self.is_bot = data['isBot']
        self.is_dead = data['isDead']

        self.champion = data['championName']
        self.level = data['level']
        self.skin_id = data['skinID']

        self.respawn_timer = data['respawnTimer']
        self.scores = GamePlayerScores(
            assists=data['scores']['assists'],
            creep_score=data['scores']['creepScore'],
            deaths=data['scores']['deaths'],
            kills=data['scores']['kills'],
            ward_score=data['scores']['wardScore']
        )

        if data.get('summonerSpells'):
            self.spells = []
            if data['summonerSpells'].get('summonerSpellOne'):
                self.spells.append(data['summonerSpells']['summonerSpellOne']['displayName'])
            if data['summonerSpells'].get('summonerSpellTwo'):
                self.spells.append(data['summonerSpells']['summonerSpellTwo']['displayName'])

        if data.get('runes'):
            self.runes = GamePlayerRunes(
                keystone=data['runes'].get('keystone'),
                primary_tree=data['runes'].get('primaryRuneTree'),
                secondary_tree=data['runes'].get('secondaryRuneTree')
            )

        if data.get('items'):
            self.items = []
            for item in data['items']:
                self.items.append(GamePlayerItem(
                    id=item['itemID'],
                    name=item['displayName'],
                    slot=item['slot'],
                    can_use=item['canUse'],
                    consumable=item['consumable'],
                    count=item['count'],
                    price=item['price']
                ))

        self.is_active_player = None
        if active_player is not None:
            self.is_active_player = False

            if active_player.name == self.summoner:
                self.is_active_player = True
                self.gold = active_player.gold
                self.champion_stats = active_player.champion_stats
                self.abilities = active_player.abilities
