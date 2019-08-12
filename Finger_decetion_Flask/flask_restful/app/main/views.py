from flask import render_template, session, redirect, url_for, current_app, request, jsonify, make_response
from werkzeug.utils import secure_filename
from . import main
from .. import db
import os
import time
from .finger_detect import detect_model

ALLOWED_EXTENSIONS = set(['png', 'jpg'])
# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 上传文件
@main.route('/detection/', methods=['GET', 'POST'], strict_slashes=False)
def api_upload():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        file_dir = current_app.config['IMG_DIR']
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        f = request.files['img']  # 从表单的file字段获取文件，myfile为该表单的name值
        print(f.filename)
        if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
            fname = secure_filename(f.filename)
            ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
            unix_time = int(time.time())
            new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
            file_path = os.path.join(file_dir, new_filename)
            f.save(file_path)  # 保存文件到upload目录
            model = detect_model(model_path=current_app.config['MODEL_PATH'])
            model.inference(file_path, current_app.config['RESULT_DIR'])
            result_path = os.path.join('img_result', str(unix_time), '0.jpg')
            return render_template('upload.html', file_name=new_filename, result_img=result_path)
        else:
            return jsonify({"code": 1001, "errmsg": "上传失败"})


#
@main.route('/', methods=['GET'])
def base():
    return render_template('base.html')


@main.route('/index/')
def index():
    pass


@main.route('/user/')
def user():
    pass


@main.route('/moderate/')
def moderate():
    pass



