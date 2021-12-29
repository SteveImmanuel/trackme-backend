from pymongo.database import Database
from trackme.database.mongo.collections.base_collection import BaseCollection


class RefreshTokens(BaseCollection):
    collection_name = 'refresh_tokens'
    # if item is a tuple, treat it as unique index
    indexes = [('hash_access', ), ('hash_refresh', )]

    def __init__(self, db: Database) -> None:
        super().__init__(db, self.collection_name)

    # no validation needed because it is not exposed to public
