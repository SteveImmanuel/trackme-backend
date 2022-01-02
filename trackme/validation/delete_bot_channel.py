from trackme.validation.base_validation import BaseValidation
from trackme.helper.validation import *


class DeleteBotChannel(BaseValidation):
    validation = {
        'id': (is_it(str), True),
    }