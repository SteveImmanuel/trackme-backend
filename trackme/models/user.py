from typing import List


class User:

    def __init__(
        self,
        username: str,
        password: str,
        alias: List[str],
        locations: List[List[str]],
        bot_channels: List[str],
    ):
        self.username = username
        self.password = password
        self.alias = alias
        self.locations = locations
        self.bot_channels = bot_channels