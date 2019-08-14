from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


# 权限装饰器
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)


# usage:
# @main.route('/admin/')
# @login_required
# @admin_required
# def for_admins_only():
#     return 'For admin...'
