from flask import Blueprint
from ..finger_detect import detect_model
from config import detection_config  # 居然根本不用..或.之类的相对路径？
detection_model = detect_model(model_path=detection_config['MODEL_PATH'])
api = Blueprint('api', __name__)
from . import authentication, pictures, users, errors


