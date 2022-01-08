from trackme.validation.base_validation import BaseValidation
from trackme.helper.validation import *


class AddBotChannel(BaseValidation):
    validation = {
        'id': (is_it(str), True),
        'type': (is_it(str), True),
        'photo_url': (is_it(str), True),
        'display_name': (is_it(str), True),
        'platform': (is_it(str), True),
    }