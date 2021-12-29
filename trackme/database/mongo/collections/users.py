from pymongo.database import Database
from trackme.helper.validation import *
from trackme.exceptions.validation_exception import ValidationException
from typing import Dict
from trackme.database.mongo.collections.base_collection import BaseCollection


class Users(BaseCollection):
    collection_name = 'users'
    # if item is a tuple, treat it as unique index
    indexes = [('username', ), 'alias', 'bot_channels']

    def __init__(self, db: Database) -> None:
        super().__init__(db, self.collection_name)

    @classmethod
    def validate_create(cls, data: Dict) -> Dict:
        validation = {
            'username': (is_string, True),
            'password': (is_password_valid, True),
            'alias': (is_list_of_string, False),
            'locations': (is_location_valid, False),
            'bot_channels': (is_list_of_string, False),
        }
        return cls.base_validate(validation, data)

    @classmethod
    def validate_update(cls, data: Dict) -> Dict:
        validation = {
            'username': (is_string, False),
            'password': (is_password_valid, False),
            'alias': (is_list_of_string, False),
            'locations': (is_location_valid, False),
            'bot_channels': (is_list_of_string, False),
        }
        return cls.base_validate(validation, data)

    @classmethod
    def validate_login(cls, data: Dict) -> Dict:
        validation = {
            'username': (is_string, True),
            'password': (is_string, True),
        }
        return cls.base_validate(validation, data)