from flask import Blueprint

# 是否导致和api模块一起加载了两个相同模型了？
# from ..finger_detect import detect_model
# from config import detection_config  # 居然根本不用..或.之类的相对路径？
# detection_model = detect_model(model_path=detection_config['MODEL_PATH'])
from ..api import detection_model

main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission


# 模板可能也需要权限控制，这里使得变量在所有模板中可访问
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
