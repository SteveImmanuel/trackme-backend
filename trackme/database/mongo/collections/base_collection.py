from pymongo.database import Database
from typing import Dict


class BaseCollection:

    def __init__(self, db: Database, collection_name: str):
        self.collection = db.get_collection(collection_name)

    def find_one(self, query: Dict) -> Dict:
        return self.collection.find_one(query)

    def create_one(self, params: Dict) -> str:
        result = self.collection.insert_one(params)
        return str(result.inserted_id)

    def delete_one(self, params: Dict) -> int:
        return self.collection.delete_one(params).deleted_count

    def update_one(self, filter: Dict, params: Dict) -> int:
        return self.collection.update_one(filter, params).modified_count