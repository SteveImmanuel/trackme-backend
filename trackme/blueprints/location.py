from flask import Blueprint, jsonify, make_response

bp = Blueprint('location', __name__, url_prefix='/location')


@bp.route('/health', methods=['POST'])
def login():
    return make_response(
        jsonify({
            'code': 200,
            'message': 'Health Check Success',
            'detail': 'Status OK'
        }), 200)
