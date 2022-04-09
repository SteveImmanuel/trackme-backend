import pytz
import trackme.bot.line_bot as LineBot

from datetime import datetime
from flask import Blueprint, jsonify, make_response, g, request
from trackme.blueprints.auth import login_required
from trackme.database.influx.location_repository import LocationRepository
from trackme.database.mongo.collections import Users
from trackme.validation.post_location import PostLocation
from trackme.exceptions.validation_exception import ValidationException
from trackme.contants import *
from trackme.helper.location import *

bp = Blueprint('location', __name__, url_prefix='/location')
location_repo = LocationRepository()
user_collection = Users()


@bp.route('', methods=['GET'])
@login_required
def get():
    try:
        result = get_last_location(g.get('uid'))

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
        location_repo.create_one(data)

        user = user_collection.find_by_id(g.get('uid'))
        if user is None:
            return make_response(
                jsonify({
                    'code': 404,
                    'message': 'Bad Request',
                    'detail': 'User not found'
                }), 404)

        last_location = get_last_location(g.get('uid'))
        location_before = get_closest_highlight_location(
            last_location.get('latitude'),
            last_location.get('longitude'),
            user.locations,
        )
        location_now = get_closest_highlight_location(
            data.get('latitude'),
            data.get('longitude'),
            user.locations,
        )

        channel_ids = map(lambda x: x.get('id'), user.bot_channels)

        if location_before != location_now:
            if location_before is not None and location_before.get('alert_on_leave'):
                LineBot.push_location_msg(
                    user.username,
                    channel_ids,
                    location_before.get('name'),
                    True,
                )
            if location_now is not None and location_now.get('alert_on_arrive'):
                LineBot.push_location_msg(
                    user.username,
                    channel_ids,
                    location_now.get('name'),
                    False,
                )

        battery_level = data.get('battery_level', 100)
        if battery_level < BATTERY_LEVEL_THRESHOLD and battery_level < last_location.get(
                'battery_level'):
            LineBot.push_low_battery_alert(user.username, channel_ids)

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
