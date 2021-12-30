from trackme.validation.base_validation import BaseValidation
from trackme.helper.validation import *


class RefreshJWTToken(BaseValidation):
    validation = {
        'refresh_token': (is_string, True),
    }
