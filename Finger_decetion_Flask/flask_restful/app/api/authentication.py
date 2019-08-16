from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from ..models import User
from . import api
from .errors import unauthorized, forbidden


auth = HTTPBasicAuth()


# 邮箱密码认证, 或是令牌认证
@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        return False
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


# 自定义401的错误响应
@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


# 蓝本所有路由前需要身份认证, 这里有待改善？
@api.before_request
@auth.login_required
def before_request():
    if g.current_user.is_anonymous:
        return forbidden('Unconfirmed account')


# 生成身份验证令牌
@api.route('/tokens/', methods=['POST'])
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(expriation=3600), 'expiration': 3600})

