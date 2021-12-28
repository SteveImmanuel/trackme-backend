import jwt
import datetime
import os

from enum import Enum
from typing import Dict

jwt_secret = os.getenv('JWT_SECRET')
jwt_expiry_time = int(os.getenv('JWT_EXPIRY_TIME'))
refresh_token_expiry_time = datetime.timedelta(days=30)

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
        data['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=jwt_expiry_time)
    else:
        data['exp'] = datetime.datetime.utcnow() + refresh_token_expiry_time

    return jwt.encode(data, jwt_secret, algorithm='HS256')

def verify_and_decode_token(token: str) -> Dict:
    return jwt.decode(token, jwt_secret, algorithms=['HS256'])