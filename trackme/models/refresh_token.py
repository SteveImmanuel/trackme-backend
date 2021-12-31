from typing import Dict
from trackme.models.base_model import BaseModel


class RefreshToken(BaseModel):

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
        return RefreshToken(data.get('uid'), data.get('hash_refresh'), data.get('hash_access'))
