import trackme.bot.line_bot as LineBot
import trackme.database.redis as redis_repository

from flask import Blueprint, jsonify, make_response, request, g
from linebot.exceptions import InvalidSignatureError
from trackme.blueprints.auth import login_required
from trackme.helper.token import generate_random_numeric_token
from trackme.constants import *

bp = Blueprint('bot', __name__, url_prefix='/bot')


@bp.route('/line', methods=['POST'])
def webhook():
    try:
        LineBot.process_webhook(request)

        return make_response(jsonify({
            'code': 200,
            'message': 'OK',
        }), 200)
    except InvalidSignatureError:
        return make_response(
            jsonify({
                'code': 400,
                'message': 'Bad Request',
                'detail': 'Invalid signature. Recheck access token and channel secret'
            }), 400)
    except Exception as e:
        print(e)
        return make_response(
            jsonify({
                'code': 500,
                'message': 'Internal Server Error',
                'detail': str(e)
            }), 500)


@bp.route('/token/channel', methods=['POST'])
@login_required
def generate_channel_token():
    try:
        uid = g.get('uid')
        channel_token = generate_random_numeric_token(4)
        redis_repository.set_key(f'channel_token_{channel_token}', uid, BOT_TOKEN_EXPIRY_TIME)
        return make_response(
            jsonify({
                'code': 200,
                'message': 'Generate Bot Token Successful',
                'detail': {
                    'token': channel_token
                }
            }), 200)
    except Exception as e:
        print(e)
        return make_response(
            jsonify({
                'code': 500,
                'message': 'Internal Server Error',
                'detail': str(e)
            }), 500)


@bp.route('/token/user', methods=['POST'])
@login_required
def generate_user_token():
    try:
        uid = g.get('uid')
        user_token = generate_random_numeric_token(4)
        redis_repository.set_key(f'user_token_{user_token}', uid, BOT_TOKEN_EXPIRY_TIME)
        return make_response(
            jsonify({
                'code': 200,
                'message': 'Generate Bot Token Successful',
                'detail': {
                    'token': user_token
                }
            }), 200)
    except Exception as e:
        return make_response(
            jsonify({
                'code': 500,
                'message': 'Internal Server Error',
                'detail': str(e)
            }), 500)