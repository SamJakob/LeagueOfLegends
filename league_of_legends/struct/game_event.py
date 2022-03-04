class GameEvent:
    """
    Represents an event that occurred in a League of Legends game, as defined
    by the League of Legends client API.
    """

    def __init__(self, data):
        self.id = data['EventID']
        self.name = data['EventName']
        self.time = data['EventTime']
