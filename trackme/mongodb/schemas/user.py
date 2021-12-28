from typing import List, Dict
from trackme.mongodb.schemas.base_schema import BaseSchema


class User(BaseSchema):

    def __init__(
        self,
        username: str,
        password: str,
        uid: str = None,
        alias: List[str] = None,
        locations: List[List[str]] = None,
        bot_channels: List[str] = None,
    ):
        self.uid = uid
        self.username = username
        self.password = password
        self.alias = alias
        self.locations = locations
        self.bot_channels = bot_channels

    def to_dict(self) -> Dict:
        return {
            'uid': self.uid,
            'username': self.username,
            'password': self.password,
            'alias': self.alias,
            'locations': self.locations,
            'bot_channels': self.bot_channels,
        }

    @staticmethod
    def from_dict(data: Dict) -> 'User':
        return User(
            data['username'],
            data['password'],
            data['_id'],
            data['alias'],
            data['locations'],
            data['bot_channels'],
        )
