from typing import Dict, List, Union
from bson.objectid import ObjectId
from trackme.database.mongo.collections.base_collection import BaseCollection
from trackme.models.user import User


class Users(BaseCollection):
    collection_name = 'users'
    # if item is a tuple, treat it as unique index
    indexes = [('username', ), 'aliases', 'bot_channels']

    def __init__(self) -> None:
        super().__init__(self.collection_name)

    def find_one(self, query: Dict) -> User:
        result = super().find_one(query)
        if result is not None:
            return User.from_dict(result)
        return None

    def find_all(self, query: Dict) -> Union[List[User], None]:
        result = super().find_all(query)
        if result:
            return [User.from_dict(item) for item in result]
        return None

    def find_by_id(self, id: str) -> User:
        return self.find_one({'_id': ObjectId(id)})
