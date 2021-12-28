from pymongo.database import Database
from trackme.helper.validation import *
from trackme.exceptions.validation_exception import ValidationException
from typing import Dict


class Users:
    collection_name = 'users'
    # if item is a tuple, treat it as unique index
    indexes = [('username', ), 'alias', 'bot_channels']
    # tuple of validator function and is required flag
    validation = {
        'username': (is_string, True),
        'password': (is_password_valid, True),
        'alias': (is_list_of_string, False),
        'locations': (is_location_valid, False),
        'bot_channels': (is_list_of_string, False),
    }

    def __init__(self, db: Database) -> None:
        self.collection = db.get_collection(self.collection_name)

    def find_one(self, query: dict) -> dict:
        return self.collection.find_one(query)

    def create_one(self, params: dict) -> str:
        result = self.collection.insert_one(params)
        return str(result.inserted_id)

    @classmethod
    def validate_create(cls, data: Dict) -> Dict:
        result = {}

        for property, (validator, is_required) in cls.validation.items():
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

    @classmethod
    def validate_update(cls, data: Dict) -> Dict:
        result = {}

        for property, (validator, _) in cls.validation.items():
            if property in data:
                try:
                    validator(data[property])
                    result[property] = data[property]
                except ValidationException as e:
                    raise ValidationException(f'Error on key \'{property}\': {e}')

        return result

    @classmethod
    def validate_login(cls, data: Dict) -> Dict:
        result = {}

        validation = {
            'username': (is_string, True),
            'password': (is_string, True),
        }

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