from typing import List, Dict
from trackme.models.base_model import BaseModel


class User(BaseModel):

    def __init__(
        self,
        uid: str,
        username: str,
        password: str,
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
            'alias': self.alias,
            'locations': self.locations,
            'bot_channels': self.bot_channels,
        }

    @staticmethod
    def from_dict(data: Dict) -> 'User':
        return User(
            str(data.get('_id')),
            data.get('username'),
            data.get('password'),
            data.get('alias', None),
            data.get('locations', None),
            data.get('bot_channels', None),
        )
