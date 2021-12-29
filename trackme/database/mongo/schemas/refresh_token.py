from typing import Dict
from trackme.database.mongo.schemas.base_schema import BaseSchema


class RefreshToken(BaseSchema):

    def __init__(self, uid: str, hash_refresh: str, hash_access: str):
        self.uid = uid
        self.hash_refresh = hash_refresh
        self.hash_access = hash_access

    def to_dict(self) -> Dict:
        return {
            'uid': self.uid,
            'hash_refresh': self.hash_refresh,
            'hash_access': self.hash_access,
        }

    @staticmethod
    def from_dict(data: Dict) -> 'RefreshToken':
        return RefreshToken(data['uid'], data['hash_refresh'], data['hash_access'])
