from typing import List, Dict
from trackme.mongodb.schemas.base_schema import BaseSchema
from trackme.helper.validation import *


class User(BaseSchema):

    def __init__(
        self,
        username: str,
        password: str,
        uid: str = None,
        alias: List[str] = None,
        locations: List[List[str]] = None,
        bot_channels: List[str] = None,
    ):
        self.uid = uid
        self.username = username
        self.password = password
        self.alias = alias
        self.locations = locations
        self.bot_channels = bot_channels
        self.validation = {
            'username': (is_string, True),
            'password': (is_password_valid, True),
            'alias': (is_list_of_string, False),
            'locations': (is_location_valid, False),
            'bot_channels': (is_list_of_string, False),
        }

    def to_dict(self) -> Dict:
        return {
            'uid': self.uid,
            'username': self.username,
            'password': self.password,
            'alias': self.alias,
            'locations': self.locations,
            'bot_channels': self.bot_channels,
        }

    @staticmethod
    def from_dict(data: Dict) -> 'User':
        return User(
            data['username'],
            data['password'],
            data['_uid'],
            data['alias'],
            data['locations'],
            data['bot_channels'],
        )

    def validate_create(self, data: Dict) -> Dict:
        result = {}

        for property, (validator, is_required) in self.validation.items():
            if property not in data:
                if is_required:
                    raise ValidationException(f'Key "{property}" is required')
            else:
                try:
                    validator(data[property])
                    result[property] = data[property]
                except ValidationException as e:
                    raise ValidationException(f'Error on key "{property}: {e}')

        return result

    def validate_update(self, data: Dict) -> Dict:
        result = {}

        for property, (validator, _) in self.validation.items():
            if property in data:
                try:
                    validator(data[property])
                    result[property] = data[property]
                except ValidationException as e:
                    raise ValidationException(f'Error on key "{property}: {e}')

        return result