from typing import Dict
from trackme.database.mongo.collections.base_collection import BaseCollection
from trackme.models.refresh_token import RefreshToken


class RefreshTokens(BaseCollection):
    collection_name = 'refresh_tokens'
    # if item is a tuple, treat it as unique index
    indexes = [('hash_access', ), ('hash_refresh', )]

    def __init__(self) -> None:
        super().__init__(self.collection_name)

    def find_one(self, query: Dict) -> RefreshToken:
        result = super().find_one(query)
        if result is not None:
            return RefreshToken.from_dict(result)
        return None
