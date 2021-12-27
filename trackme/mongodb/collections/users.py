from pymongo.database import Database


class Users:
    collection_name = 'users'
    indexes = ['username']

    def __init__(self, db: Database) -> None:
        self.collection = db.get_collection(self.collection_name)

    def findOne(self, query: dict) -> dict:
        return self.collection.find_one(query)