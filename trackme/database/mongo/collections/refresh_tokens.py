from pymongo.database import Database
from trackme.database.mongo.collections.base_collection import BaseCollection


class RefreshTokens(BaseCollection):
    collection_name = 'refresh_tokens'
    indexes = ['hash']

    def __init__(self, db: Database) -> None:
        super().__init__(db, self.collection_name)