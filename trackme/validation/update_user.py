from trackme.validation.base_validation import BaseValidation
from trackme.helper.validation import *


class UpdateUser(BaseValidation):
    validation = {
        'username': (is_it(str), False),
        'password': (is_password_valid, False),
        'alias': ([is_it(str)], False),
        'locations': (
            [{
                'latitude': (is_latitude_valid, True),
                'longitude': (is_longitude_valid, True),
                'type': (is_it(str), True),
                'alert_on_leave': (is_it(bool), True),
                'alert_on_arrive': (is_it(bool), True),
            }],
            False,
        ),
        'bot_channels': ([is_it(str)], False),
    }