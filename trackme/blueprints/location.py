import pytz
import trackme.database.redis as redis_repository

from typing import Dict, Union
from datetime import datetime
from flask import Blueprint, jsonify, make_response, g, request
from trackme.blueprints.auth import login_required
from trackme.database.influx.location_repository import LocationRepository
from trackme.validation.post_location import PostLocation
from trackme.exceptions.validation_exception import ValidationException
from trackme.contants import *

bp = Blueprint('location', __name__, url_prefix='/location')
location_repo = LocationRepository()


def set_location_cache(data: Dict) -> None:
    hash_key = 'location_' + data.get('uid')
    for key, value in data.items():
        redis_repository.hset_key(hash_key, key, value)


def get_location_cache(uid: str) -> Union[None, Dict]:
    hash_key = 'location_' + uid
    if not redis_repository.is_key_exist(hash_key):
        return None
    data = {}
    data['uid'] = redis_repository.hget_key(hash_key, 'uid')
    data['longitude'] = redis_repository.hget_key(hash_key, 'longitude')
    data['latitude'] = redis_repository.hget_key(hash_key, 'latitude')
    data['timestamp'] = redis_repository.hget_key(hash_key, 'timestamp')
    return data


@bp.route('', methods=['GET'])
@login_required
def get():
    try:
        data = {'uid': g.get('uid'), 'start': '-1w'}

        # get from cache if exist
        result = get_location_cache(g.get('uid'))
        if result is None:
            result = location_repo.find_latest_one(data)
            result.timestamp = result.timestamp.astimezone(pytz.timezone(TIMEZONE))
            result.timestamp = result.timestamp.strftime('%a, %d %b %I:%M %p')
            result = result.to_dict()
            set_location_cache(result)

        if result is None:
            return make_response(
                jsonify({
                    'code': 404,
                    'message': 'Not Found',
                    'detail': 'Location log not found within one week'
                }), 404)

        return make_response(
            jsonify({
                'code': 200,
                'message': 'Get Location Successful',
                'detail': result
            }), 200)

    except Exception as e:
        return make_response(
            jsonify({
                'code': 500,
                'message': 'Internal Server Error',
                'detail': str(e)
            }), 500)


@bp.route('', methods=['POST'])
@login_required
def post():
    try:
        data = PostLocation.validate(request.json)
        data['uid'] = g.get('uid')
        datetime.now()
        location_repo.create_one(data)

        # save to cache
        now = datetime.now(tz=pytz.timezone(TIMEZONE))
        data['timestamp'] = now.strftime('%a, %d %b %I:%M %p')
        set_location_cache(data)

        return make_response(
            jsonify({
                'code': 200,
                'message': 'Post Location Successful',
                'detail': data
            }), 200)
    except ValidationException as e:
        return make_response(jsonify({
            'code': 400,
            'message': 'Bad Request',
            'detail': str(e)
        }), 400)
    except Exception as e:
        return make_response(
            jsonify({
                'code': 500,
                'message': 'Internal Server Error',
                'detail': str(e)
            }), 500)
