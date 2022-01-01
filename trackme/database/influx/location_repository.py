from typing import Dict, Union
from trackme.database.influx.base_repository import BaseRepository
from trackme.models.location import Location


class LocationRepository(BaseRepository):

    def create_one(self, data: Dict) -> None:
        super().create_one(
            'coordinates',
            {
                'uid': data.get('uid'),
            },
            {
                'longitude': data.get('longitude'),
                'latitude': data.get('latitude'),
            },
        )

    def find_latest_one(self, data: Dict) -> Union[Location, None]:
        records = super().find_latest_one(
            'coordinates',
            {
                'uid': data.get('uid'),
            },
            data.get('start', '-1d'),
        )

        longitude = latitude = None
        for record in records:
            if record.get_field() == 'longitude':
                longitude = record.get_value()
            elif record.get_field() == 'latitude':
                latitude = record.get_value()
            timestamp = record.get_time()

        if longitude is not None and latitude is not None:
            return Location(data.get('uid'), timestamp, longitude, latitude)
        return None
