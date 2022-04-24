from trackme.validation.base_validation import BaseValidation
from trackme.helper.validation import *


class UpdateUser(BaseValidation):
    validation = {
        'username': (is_it(str), False),
        'password': (is_password_valid, False),
        'aliases': ([is_it(str)], False),
        'locations': (
            [{
                'latitude': (is_latitude_valid, True),
                'longitude': (is_longitude_valid, True),
                'name': (is_it(str), True),
                'alert_on_leave': (is_it(bool), True),
                'alert_on_arrive': (is_it(bool), True),
            }],
            False,
        ),
        'bot_channels': (
            [{
                'id': (is_it(str), True),
                'type': (is_it(str), True),
                'photo_url': (is_it(str), False),
                'display_name': (is_it(str), True),
                'platform': (is_it(str), True),
                'indirect_mention_notif': (is_it(bool), True),
            }],
            False,
        ),
        'linked_accounts:': (
            [{
                'id': (is_it(str), True),
                'platform': (is_it(str), True),
                'photo_url': (is_it(str), False),
                'display_name': (is_it(str), True),
            }],
            False,
        ),
    }