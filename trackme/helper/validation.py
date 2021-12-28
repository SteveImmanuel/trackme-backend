from typing import Any
from trackme.exceptions.validation_exception import ValidationException

def is_numeric(value: Any) -> None:
    str_value = str(value)
    if not str_value.isnumeric():
        raise ValidationException('Value must be numeric')

def is_string(value: Any) -> None:
    if not isinstance(value, str):
        raise ValidationException('Value must be a string')

def is_list_of_string(value: Any) -> None:
    if not isinstance(value, list):
        raise ValidationException('Value must be a list')
    for alias in value:
        if not isinstance(alias, str):
            raise ValidationException('Value must be a string')
    return True

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
    return True

def is_location_valid(value: Any) -> None:
    if not isinstance(value, list):
        raise ValidationException('Value must be a list')
    if len(value) != 2:
        raise ValidationException('Value must consists of latitude and longitude')
    lat, long = value
    if not isinstance(lat, str) or not isinstance(long, str):
        raise ValidationException('Latitude and longitude must be numeric strings')
    if not lat.isnumeric() or not long.isnumeric():
        raise ValidationException('Latitude and longitude must be numeric strings')
    if float(lat) < -90 or float(lat) > 90:
        raise ValidationException('Latitude must be between -90 and 90')
    if float(long) < -180 or float(long) > 180:
        raise ValidationException('Longitude must be between -180 and 180')
    return True
