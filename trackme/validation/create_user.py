from trackme.validation.base_validation import BaseValidation
from trackme.helper.validation import *


class CreateUser(BaseValidation):
    validation = {
        'username': (is_string, True),
        'password': (is_password_valid, True),
        'alias': (is_list_of_string, False),
        'locations': (is_location_valid, False),
        'bot_channels': (is_list_of_string, False),
    }