import math
import pytz

from typing import Dict, Union, List
import trackme.database.redis as redis_repository
from trackme.database.influx.location_repository import LocationRepository
from trackme.contants import TIMEZONE, THRESHOLD_DISTANCE

location_repo = LocationRepository()
EARTH_RADIUS = 6378137 # in m

def calculate_distance(lat1, long1, lat2, long2):
    delta_lat = math.radians(lat2 - lat1)
    delta_long = math.radians(long2 - long1)

    a = math.sin(delta_lat / 2) * math.sin(delta_lat / 2) + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)) * math.sin(delta_long / 2) * math.sin(delta_long / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return EARTH_RADIUS * c
    
def set_location_cache(data: Dict) -> None:
    hash_key = 'location_' + data.get('uid')
    for key, value in data.items():
        redis_repository.hset_key(hash_key, key, value)


def get_last_location(uid: str) -> Union[None, Dict]:
    hash_key = 'location_' + uid
    if not redis_repository.is_key_exist(hash_key):
        query = {'uid': uid, 'start': '-1w'}
        result = location_repo.find_latest_one(query)
        result.timestamp = result.timestamp.astimezone(pytz.timezone(TIMEZONE))
        result.timestamp = result.timestamp.strftime('%a, %d %b %I:%M %p')
        result = result.to_dict()
        set_location_cache(result)
        return None

    data = {}
    data['uid'] = redis_repository.hget_key(hash_key, 'uid')
    data['longitude'] = redis_repository.hget_key(hash_key, 'longitude')
    data['latitude'] = redis_repository.hget_key(hash_key, 'latitude')
    data['timestamp'] = redis_repository.hget_key(hash_key, 'timestamp')
    return data


def get_closest_highlight_location(latitude: Union[float, str], longitude: Union[float, str],
                                   locations: List[Dict]) -> Union[Dict, None]:
    min_dist = math.inf
    latitude = float(latitude)
    longitude = float(longitude)
    idx = -1
    for index, location in enumerate(locations):
        current_dist = calculate_distance(
            latitude,
            longitude,
            float(location.get('latitude')),
            float(location.get('longitude')),
        )
        if current_dist < min_dist:
            min_dist = current_dist
            idx = index
    if idx != -1 and min_dist <= THRESHOLD_DISTANCE:
        return locations[idx]
    return None