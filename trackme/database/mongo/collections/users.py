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