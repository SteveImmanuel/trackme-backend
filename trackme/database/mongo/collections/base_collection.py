from pymongo.database import Database
from typing import Dict
from trackme.exceptions.validation_exception import ValidationException


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

    @classmethod
    def base_validate(cls, validation: Dict, data: Dict) -> Dict:
        """
        validation is a dict where each item consists of 
        a tuple of validator function and is required flag
        """
        result = {}

        for property, (validator, is_required) in validation.items():
            if property not in data:
                if is_required:
                    raise ValidationException(f'Key \'{property}\' is required')
            else:
                try:
                    validator(data[property])
                    result[property] = data[property]
                except ValidationException as e:
                    raise ValidationException(f'Error on key \'{property}\': {e}')

        return result