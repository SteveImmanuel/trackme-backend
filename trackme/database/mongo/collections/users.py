from typing import Dict
from trackme.database.mongo.collections.base_collection import BaseCollection
from trackme.models.user import User


class Users(BaseCollection):
    collection_name = 'users'
    # if item is a tuple, treat it as unique index
    indexes = [('username', ), 'alias', 'bot_channels']

    def __init__(self) -> None:
        super().__init__(self.collection_name)

    def find_one(self, query: Dict) -> User:
        result = super().find_one(query)
        if result is not None:
            return User.from_dict(result)
        return None
