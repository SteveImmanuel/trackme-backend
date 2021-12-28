from pymongo.database import Database


class RefreshTokens:
    collection_name = 'refresh_tokens'
    indexes = ['hash']

    def __init__(self, db: Database) -> None:
        self.collection = db.get_collection(self.collection_name)

    def findOne(self, query: dict) -> dict:
        return self.collection.find_one(query)