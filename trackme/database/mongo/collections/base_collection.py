from typing import Dict
import trackme.database.mongo as mongo_db


class BaseCollection:

    def __init__(self, collection_name: str):
        self.collection = mongo_db.db.get_collection(collection_name)

    def find_one(self, query: Dict) -> Dict:
        return self.collection.find_one(query)

    def create_one(self, params: Dict) -> str:
        result = self.collection.insert_one(params)
        return str(result.inserted_id)

    def delete_one(self, params: Dict) -> int:
        return self.collection.delete_one(params).deleted_count

    def update_one(self, filter: Dict, params: Dict) -> Dict:
        result = self.collection.update_one(filter, params).raw_result
        formatted_result = {
            'total_matched': result.get('n'),
            'total_modified': result.get('nModified'),
        }
        return formatted_result