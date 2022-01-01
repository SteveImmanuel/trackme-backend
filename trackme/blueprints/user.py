from flask import Blueprint, jsonify, make_response, g, request
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from trackme.blueprints.auth import login_required
from trackme.database.mongo.collections import Users
from trackme.validation import UpdateUser
from trackme.exceptions.validation_exception import ValidationException

bp = Blueprint('user', __name__, url_prefix='/user')

user_collection = Users()


@bp.route('', methods=['GET'])
@login_required
def get():
    try:
        user = user_collection.find_one({'_id': ObjectId(g.get('uid'))})

        if user is None:
            return make_response(
                jsonify({
                    'code': 404,
                    'message': 'Not Found',
                    'detail': 'User not found'
                }), 404)

        return make_response(
            jsonify({
                'code': 200,
                'message': 'Get User Successful',
                'detail': user.to_dict(),
            }), 200)
    except Exception as e:
        return make_response(
            jsonify({
                'code': 500,
                'message': 'Internal Server Error',
                'detail': str(e)
            }), 500)


@bp.route('', methods=['PUT'])
@login_required
def update():
    try:
        data = UpdateUser.validate(request.json)
        result = user_collection.update_one({'_id': ObjectId(g.get('uid'))}, {'$set': data})
        if result.get('n') == 0:
            return make_response(
                jsonify({
                    'code': 404,
                    'message': 'Not Found',
                    'detail': 'User not found'
                }), 404)

        return make_response(
            jsonify({
                'code': 200,
                'message': 'Update User Successful',
                'detail': result
            }), 200)
    except ValidationException as e:
        return make_response(jsonify({
            'code': 400,
            'message': 'Bad Request',
            'detail': str(e)
        }), 400)
    except DuplicateKeyError as e:
        return make_response(
            jsonify({
                'code': 400,
                'message': 'Bad Request',
                'detail': 'Username already taken'
            }), 400)
    except Exception as e:
        return make_response(
            jsonify({
                'code': 500,
                'message': 'Internal Server Error',
                'detail': str(e)
            }), 500)