from trackme.validation.base_validation import BaseValidation
from trackme.helper.validation import *


class PostLocation(BaseValidation):
    validation = {
        'latitude': (is_latitude_valid, True),
        'longitude': (is_longitude_valid, True),
        'battery_level': (is_it(int), False),
    }
