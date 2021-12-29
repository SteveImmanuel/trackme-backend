import functools
import trackme.database.mongo as mongo_db
import trackme.database.redis as redis_db

from pymongo.errors import DuplicateKeyError
from jwt import ExpiredSignatureError, InvalidTokenError
from flask import Blueprint, g, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from trackme.helper.token import *
from trackme.database.mongo.collections import Users, RefreshTokens
from trackme.exceptions.validation_exception import ValidationException
from trackme.contants import *

bp = Blueprint('auth', __name__, url_prefix='/auth')
user_collection = Users(mongo_db.db)
refresh_token_collection = RefreshTokens(mongo_db.db)


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


@bp.route('/login', methods=['POST'])
def login():
    try:
        data = user_collection.validate_login(request.json)
        user = user_collection.find_one({'username': data['username']})

        if user is not None:
            if check_password_hash(user['password'], data['password']):
                uid = str(user['_id'])
                access_token = generate_token(uid, TokenType.ACCESS)
                refresh_token = generate_token(uid, TokenType.REFRESH)

                h_access_token = get_hash(access_token)
                h_refresh_token = get_hash(refresh_token)
                refresh_token_collection.create_one({
                    'uid': uid,
                    'hash_refresh': h_refresh_token,
                    'hash_access': h_access_token
                })

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


@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    try:
        # add hash value of access token to token blacklist in redis
        hash_token = get_hash(g.get('access_token', ''))
        redis_db.set_key(hash_token, '1', JWT_EXPIRY_TIME)

        # delete refresh token in mongo
        refresh_token_collection.delete_one({'hash_access': hash_token})

        return make_response(jsonify({'code': 200, 'message': 'Logout Successful'}), 200)
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
            is_revoked = redis_db.get_key(get_hash(access_token))
            if is_revoked is None:
                decoded_token = verify_and_decode_token(access_token)
                g.uid = decoded_token['uid']
                g.access_token = access_token
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
                'code': 400,
                'message': 'Bad Request',
                'detail': 'Unsupported format of authorization header'
            }), 400)


@bp.route('/test', methods=['GET'])
@login_required
def test():
    id = request.args['id']
    user = user_collection.find_one({'_id': ObjectId(id)})
    print(user)
    return make_response(jsonify({"message": "test successful", 'uid': None}), 200)
