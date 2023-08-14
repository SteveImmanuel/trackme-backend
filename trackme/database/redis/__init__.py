import redis
from typing import Union
from trackme.constants import *

# initialize connection
client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


def set_key(key: str, value: str, expiry_time: int = REDIS_DEFAULT_EXPIRY_TIME) -> None:
    client.setex(key, expiry_time, value.encode('utf-8'))


def get_key(key: str) -> Union[str, None]:
    value = client.get(key)
    if value:
        return value.decode('utf-8')
    return None


def hset_key(hash: str, key: str, value: str, expiry_time: int = REDIS_DEFAULT_EXPIRY_TIME):
    client.hset(hash, key, value.encode('utf-8'))
    client.expire(hash, expiry_time)


def hget_key(hash: str, key: str) -> Union[str, None]:
    value = client.hget(hash, key)
    if value:
        return value.decode('utf-8')
    return None


def is_key_exist(key: str) -> int:
    return client.exists(key)