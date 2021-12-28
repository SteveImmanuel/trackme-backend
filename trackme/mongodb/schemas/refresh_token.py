from typing import Dict
from trackme.mongodb.schemas.base_schema import BaseSchema


class RefreshToken(BaseSchema):

    def __init__(
        self,
        uid: str,
        hash: str,
    ):
        self.uid = uid
        self.hash = hash

    def to_dict(self) -> Dict:
        return {
            'uid': self.uid,
            'hash': self.hash,
        }

    @staticmethod
    def from_dict(data: Dict) -> 'RefreshToken':
        return RefreshToken(
            data['uid'],
            data['hash'],
        )

    # no validation needed because it is not exposed to public