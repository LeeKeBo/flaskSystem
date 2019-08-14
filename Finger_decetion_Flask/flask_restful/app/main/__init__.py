from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission


# 模板可能也需要权限控制，这里使得变量在所有模板中可访问
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
