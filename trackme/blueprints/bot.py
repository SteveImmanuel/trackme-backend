import trackme.bot.line_bot as LineBot
import trackme.database.redis as redis_repository

from flask import Blueprint, jsonify, make_response, request, g
from linebot.exceptions import InvalidSignatureError
from trackme.blueprints.auth import login_required
from trackme.helper.token import generate_random_numeric_token
from trackme.contants import *

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


@bp.route('/token', methods=['POST'])
@login_required
def generate_token():
    try:
        uid = g.get('uid')
        bot_token = generate_random_numeric_token(4)
        redis_repository.set_key(f'bot_token_{bot_token}', uid, BOT_TOKEN_EXPIRY_TIME)
        return make_response(
            jsonify({
                'code': 200,
                'message': 'Generate Bot Token Successful',
                'detail': {
                    'token': bot_token
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
