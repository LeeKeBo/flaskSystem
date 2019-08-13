from flask import render_template, request, jsonify


# 这里的错误由Web生成，故写辅助函数用以视图函数调用
def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response

