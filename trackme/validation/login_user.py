from trackme.validation.base_validation import BaseValidation
from trackme.helper.validation import *


class LoginUser(BaseValidation):
    validation = {
        'username': (is_string, True),
        'password': (is_string, True),
    }
