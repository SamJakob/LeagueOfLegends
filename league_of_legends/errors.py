class ClientConnectError(Exception):
    """
    Raised when a connection cannot be made to the client.
    This is likely because a game is not in progress, but it can also be
    because of OS-level restrictions such as permissions issues or a
    firewall.
    """

    def __init__(self, host, message="Failed to connect to the League of Legends client. "
                                     "It seems there is no game in progress."):
        self.host = host
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f'{self.host} -> {self.message}'
