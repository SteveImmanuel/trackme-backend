from typing import List, Dict
from trackme.models.base_model import BaseModel


class User(BaseModel):

    def __init__(
        self,
        uid: str,
        username: str,
        password: str,
        aliases: List[str] = None,
        locations: List[Dict] = None,
        bot_channels: List[Dict] = None,
        connected_accounts: List[Dict] = None,
    ):
        self.uid = uid
        self.username = username
        self.password = password
        self.aliases = aliases
        self.locations = locations
        self.bot_channels = bot_channels
        self.connected_accounts = connected_accounts

    def to_dict(self) -> Dict:
        return {
            'uid': self.uid,
            'username': self.username,
            'aliases': self.aliases,
            'locations': self.locations,
            'bot_channels': self.bot_channels,
            'connected_accounts': self.connected_accounts,
        }

    @staticmethod
    def from_dict(data: Dict) -> 'User':
        return User(
            str(data.get('_id')),
            data.get('username'),
            data.get('password'),
            data.get('aliases', None),
            data.get('locations', None),
            data.get('bot_channels', None),
            data.get('connected_accounts', None),
        )
