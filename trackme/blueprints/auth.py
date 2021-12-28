import trackme.mongodb as mongodb
import functools
from pymongo.errors import DuplicateKeyError
from jwt import ExpiredSignatureError, InvalidTokenError
from flask import Blueprint, g, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from trackme.helper.token import *
from trackme.mongodb.collections import Users
from trackme.exceptions.validation_exception import ValidationException

bp = Blueprint('auth', __name__, url_prefix='/auth')
db_connection = mongodb.db
user_collection = Users(db_connection)


@bp.route('/login', methods=['POST'])
def login():
    try:
        data = user_collection.validate_login(request.json)
        user = user_collection.find_one({'username': data['username']})

        if user is not None:
            if check_password_hash(user['password'], data['password']):
                uid = str(user['_id'])
                print(uid)
                access_token = generate_token(uid, TokenType.ACCESS)
                print(access_token)
                refresh_token = generate_token(uid, TokenType.REFRESH)
                print(refresh_token)
                return make_response(
                    jsonify({
                        'code': 200,
                        'message': 'Login Successful',
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    }), 200)
        return make_response(
            jsonify({
                'code': 403,
                'message': 'Login Failed',
                'detail': 'Wrong username/password'
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


@bp.route('/register', methods=['POST'])
def register():
    try:
        data = user_collection.validate_create(request.json)
        data['password'] = generate_password_hash(data['password'])
        user_collection.create_one(data)
        return make_response(jsonify({'code': 200, 'message': 'Register Successful'}), 200)
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


@bp.before_app_request
def load_jwt():
    try:
        authorization_header = request.headers.get('Authorization', None)
        if authorization_header is not None:
            access_token = request.headers.get('Authorization').split(' ')[1]
            decoded_token = verify_and_decode_token(access_token)
            g.uid = decoded_token['uid']
    except ExpiredSignatureError as e:
        return make_response(
            jsonify({
                'code': 401,
                'message': 'Unauthorized',
                'detail': 'Token expired'
            }), 401)
    except InvalidTokenError as e:
        return make_response(
            jsonify({
                'code': 401,
                'message': 'Unauthorized',
                'detail': 'Token invalid'
            }), 401)
    except IndexError as e:
        return make_response(
            jsonify({
                'code': 401,
                'message': 'Unauthorized',
                'detail': 'Unsupported format of authorization header'
            }), 401)


def login_required(function):

    @functools.wraps(function)
    def wrapped_view(**kwargs):
        if g.get('uid', None) is None:
            return make_response(
                jsonify({
                    'code': 401,
                    'message': 'Unauthorized',
                    'detail': 'You are not logged in'
                }), 401)

        return function(**kwargs)

    return wrapped_view


@bp.route('/test', methods=['GET'])
@login_required
def test():
    id = request.args['id']
    user = user_collection.find_one({'_id': ObjectId(id)})
    print(user)
    return make_response(jsonify({"message": "test successful", 'uid': None}), 200)
