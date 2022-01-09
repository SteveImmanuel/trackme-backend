from typing import Dict, Any, Union, Callable
from trackme.exceptions.validation_exception import ValidationException


class BaseValidation:
    validation = {}

    @classmethod
    def validate(cls, data: Any, validation: Union[Dict, Callable] = None) -> Dict:
        """
        validation is a dict where each item consists of 
        a tuple of validator function and is required flag
        OR
        a function with single parameter
        """
        if validation is None:
            validation = cls.validation

        if isinstance(validation, Dict):
            if not isinstance(data, dict):
                raise ValidationException('Data must be a valid JSON object')
            result = {}

            for property, (validator, is_required) in validation.items():
                if property not in data:
                    if is_required:
                        raise ValidationException(f'Key \'{property}\' is required')
                else:
                    try:
                        if isinstance(validator, list):
                            if len(validator) != 1 and not callable(
                                    validator[0]) and not isinstance(validator[0], dict):
                                raise Exception(
                                    f'Unsupported validation on key \'{property}\', validator must be single element list of dict or function'
                                )

                            if not isinstance(data[property], list):
                                raise ValidationException(
                                    f'Error on key \'{property}\': Value must be a list')

                            if len(data[property]) == 0:
                                result[property] = []
                            else:
                                property_value = []
                                for idx, item in enumerate(data[property]):
                                    try:
                                        property_value.append(cls.validate(item, validator[0]))
                                        result[property] = property_value
                                    except ValidationException as e:
                                        raise ValidationException(f'On index-{idx}: {e}')

                        elif isinstance(validator, dict):
                            result[property] = cls.validate(data[property], validator)
                        elif callable(validator):
                            validator(data[property])
                            result[property] = data[property]
                        else:
                            raise Exception(
                                f'Unsupported validation list on key \'{property}\', expected list, dict, or function, got {type(validator)}'
                            )
                    except ValidationException as e:
                        raise ValidationException(f'Error on key \'{property}\': {e}')

            return result

        elif callable(validation):
            validation(data)
            return data
        else:
            raise Exception(
                f'Unsupported validation \'dict\' or \'function\', got {type(validation).__name__}')
