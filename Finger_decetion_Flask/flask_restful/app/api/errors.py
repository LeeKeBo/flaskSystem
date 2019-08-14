from flask import jsonify
from ..exceptions import ValidationError
from . import api


# 这里的错误由Web生成，故写辅助函数用以视图函数调用
def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
