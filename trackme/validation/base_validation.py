from typing import Dict, Any
from trackme.exceptions.validation_exception import ValidationException


class BaseValidation:
    validation = {}

    @classmethod
    def validate(cls, data: Any) -> Dict:
        """
        validation is a dict where each item consists of 
        a tuple of validator function and is required flag
        """
        if not isinstance(data, dict):
            raise ValidationException('Request body must be a json object')
        result = {}

        for property, (validator, is_required) in cls.validation.items():
            if property not in data:
                if is_required:
                    raise ValidationException(f'Key \'{property}\' is required')
            else:
                try:
                    validator(data[property])
                    result[property] = data[property]
                except ValidationException as e:
                    raise ValidationException(f'Error on key \'{property}\': {e}')

        return result