from trackme.validation.base_validation import BaseValidation
from trackme.helper.validation import *


class UpdateUser(BaseValidation):
    validation = {
        'username': (is_string, False),
        'password': (is_password_valid, False),
        'alias': (is_list_of_string, False),
        'locations': (is_location_valid, False),
        'bot_channels': (is_list_of_string, False),
    }