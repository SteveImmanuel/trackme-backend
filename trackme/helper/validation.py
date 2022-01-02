from typing import Any
from trackme.exceptions.validation_exception import ValidationException

def is_it(var_type: type) -> None:
    def wrapper(value: Any):
        if not isinstance(value, var_type):
            raise ValidationException(f'Value must be a {var_type.__name__}')
    return wrapper

def is_numeric(value: Any) -> None:
    try:
        float(value)
    except:
        raise ValidationException('Value must be numeric')

def is_password_valid(value: Any) -> None:
    if not isinstance(value, str):
        raise ValidationException('Value must be a string')
    if len(value) < 8:
        raise ValidationException('Value must be at least 8 characters long')
    if not any(char.isdigit() for char in value):
        raise ValidationException('Value must contain at least one number')
    if not any(char.isupper() for char in value):
        raise ValidationException('Value must contain at least one uppercase letter')
    if not any(char.islower() for char in value):
        raise ValidationException('Value must contain at least one lowercase letter')

def is_coordinate_valid(value: Any, min_val:float, max_val:float) -> None:
    is_numeric(value)
    if float(value) < min_val or float(value) > max_val:
        raise ValidationException(f'Value must be between {min_val} and {max_val}')

def is_latitude_valid(value: Any) -> None:
    is_coordinate_valid(value, -90, 90)

def is_longitude_valid(value: Any) -> None:
    is_coordinate_valid(value, -180, 180)