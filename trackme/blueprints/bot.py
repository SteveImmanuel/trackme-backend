from flask import Blueprint, jsonify, make_response, request
from linebot.exceptions import InvalidSignatureError
import trackme.bot.line_bot as Bot

bp = Blueprint('bot', __name__, url_prefix='/bot')


@bp.route('/webhook', methods=['POST'])
def webhook():
    try:
        Bot.process_webhook(request)

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
