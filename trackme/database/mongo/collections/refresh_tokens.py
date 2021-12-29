from pymongo.database import Database
from trackme.database.mongo.collections.base_collection import BaseCollection
from trackme.helper.validation import *
from trackme.exceptions.validation_exception import ValidationException
from typing import Dict


class RefreshTokens(BaseCollection):
    collection_name = 'refresh_tokens'
    # if item is a tuple, treat it as unique index
    indexes = [('hash_access', ), ('hash_refresh', )]

    def __init__(self, db: Database) -> None:
        super().__init__(db, self.collection_name)

    @classmethod
    def validate_refresh(cls, data: Dict) -> Dict:
        validation = {
            'refresh_token': (is_string, True),
        }
        return cls.base_validate(validation, data)
