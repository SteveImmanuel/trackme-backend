import jwt
import datetime
import hashlib

from enum import Enum
from typing import Dict
from trackme.contants import *

class TokenType(Enum):
    ACCESS = 'access'
    REFRESH = 'refresh'

def generate_token(uid: str, type: TokenType) -> str:
    data = {
        'uid': uid,
        'iat': datetime.datetime.utcnow(),
        'type': type.value
    }

    if type == TokenType.ACCESS:
        data['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXPIRY_TIME)
    else:
        data['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=30)

    return jwt.encode(data, JWT_SECRET, algorithm='HS256')

def verify_and_decode_token(token: str) -> Dict:
    return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])

def get_hash(token: str) -> str:
    return hashlib.md5(token.encode('utf-8')).hexdigest()