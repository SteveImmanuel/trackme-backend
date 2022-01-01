from flask import Blueprint, jsonify, make_response, g, request
from flask.wrappers import Request
from trackme.blueprints.auth import login, login_required
from trackme.database.influx.location_repository import LocationRepository
from trackme.validation.post_location import PostLocation
from trackme.exceptions.validation_exception import ValidationException

bp = Blueprint('location', __name__, url_prefix='/location')
location_repo = LocationRepository()


@bp.route('', methods=['GET'])
@login_required
def get():
    try:
        data = {'uid': g.get('uid'), 'start': '-1w'}

        #TODO: get from cache if exist
        print(data)

        result = location_repo.find_latest_one(data)
        print(result)
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
                'detail': result.to_dict()
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

        #TODO: save to cache

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
