from flask import request, g, current_app, Response
from werkzeug.utils import secure_filename
from .. import db
from ..models import Picture, Permission
from .decorators import permission_required
from . import api, detection_model
from .errors import bad_request
import os
import time
import base64

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 用字节流返回？有待商榷
@api.route('/detection/', methods=['POST'])
@permission_required(Permission.UPLOAD)
def detection():
    # 存放图片的目录
    file_dir = current_app.config['IMG_DIR']
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    # 获取图片
    upload_file = request.files['file']
    if not allowed_file(upload_file.filename):
        return bad_request('Invalid File, it is not .jpg or .png !')
    # 改名
    fname = secure_filename(upload_file.filename)
    ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
    unix_time = int(time.time())
    new_filename = str(unix_time) + '.' + ext
    # 保存图片
    file_path = os.path.join(file_dir, new_filename)
    upload_file.save(file_path)
    # 将图片存入数据库
    picture = Picture(pic_name=new_filename, user=g.current_user)
    db.session.add(picture)
    db.session.commit()
    # 模型检测
    if len(request.form) != 0:
        top_b = int(request.form['top_b'])
        bottom_b = int(request.form['bottom_b'])
        left_b = int(request.form['left_b'])
        right_b = int(request.form['right_b'])
        # print(top_b, bottom_b, left_b, right_b)
        detection_model.inference(file_path, current_app.config['RESULT_DIR'],
                                  top_b=top_b, bottom_b=bottom_b,
                                  left_b=left_b, right_b=right_b)
    else:
        detection_model.inference(file_path, current_app.config['RESULT_DIR'])
    # 以static为根目录的相对路径, 这里只是返回一个子图, 虽然大多情况下都应该只有一个子图
    result_path = os.path.join(current_app.config['RESULT_DIR'], str(unix_time), '0.jpg')
    # print(result_path)
    image = open(result_path, 'rb')
    # res = Response(image, mimetype="image/jpeg")
    res = base64.b64encode(image.read())
    return res


# usage:
# http --auth 13798282351@qq.com:123456 http://localhost:5000/api/v1/picture > ***.jpg
# failure
