from typing import Dict
from trackme.models.base_model import BaseModel
from datetime import datetime


class Location(BaseModel):

    def __init__(self, uid: str, timestamp: datetime, longitude: str, latitude: str):
        self.uid = uid
        self.timestamp = timestamp
        self.longitude = longitude
        self.latitude = latitude

    def to_dict(self) -> Dict:
        return {
            'uid': self.uid,
            'timestamp': self.timestamp,
            'longitude': self.longitude,
            'latitude': self.latitude,
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Location':
        return Location(
            data.get('uid'),
            data.get('timestamp'),
            data.get('longitude'),
            data.get('latitude'),
        )
