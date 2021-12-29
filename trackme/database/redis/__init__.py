import redis
from typing import Union
from trackme.contants import *

# initialize connection
client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


def set_key(key: str, value: str, expiry_time: int = REDIS_DEFAULT_EXPIRY_TIME) -> None:
    client.setex(key, expiry_time, value.encode('utf-8'))


def get_key(key: str) -> Union[str, None]:
    value = client.get(key)
    if value:
        return value.decode('utf-8')
    return None