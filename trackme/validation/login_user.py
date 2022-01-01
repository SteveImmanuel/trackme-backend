from trackme.validation.base_validation import BaseValidation
from trackme.helper.validation import *


class LoginUser(BaseValidation):
    validation = {
        'username': (is_it(str), True),
        'password': (is_it(str), True),
    }
