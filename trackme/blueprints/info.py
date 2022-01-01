from flask import Blueprint, jsonify, make_response

bp = Blueprint('info', __name__, url_prefix='/')


@bp.route('/health', methods=['GET'])
def login():
    return make_response(
        jsonify({
            'code': 200,
            'message': 'Health Check Success',
            'detail': 'Status OK'
        }), 200)
