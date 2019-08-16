from flask import render_template, current_app
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from . import main
from .. import db
from .. models import Picture
import os
import time
from .finger_detect import detect_model
from .forms import PictureForm


# 上传文件, 未重定向, 无法在网页刷新？
@main.route('/detection/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def detection():
    form = PictureForm()
    if form.validate_on_submit():
        # 存放图片的目录
        file_dir = current_app.config['IMG_DIR']
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        # 图片名是否正确
        pic = form.pic.data
        # 改名
        fname = secure_filename(pic.filename)
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = str(unix_time) + '.' + ext
        # 保存图片
        file_path = os.path.join(file_dir, new_filename)
        pic.save(file_path)
        # 将图片存入数据库
        picture = Picture(pic_name=new_filename, user=current_user)
        db.session.add(picture)
        db.session.commit()
        # 模型检测
        model = detect_model(model_path=current_app.config['MODEL_PATH'])
        model.inference(file_path, current_app.config['RESULT_DIR'],
                        bottom_b=form.Bottom_b.data, top_b=form.Top_b.data,
                        left_b=form.Left_b.data, right_b=form.Right_b.data)
        # 以static为根目录的相对路径, 这里只是返回一个子图, 虽然大多情况下都应该只有一个子图
        result_path = os.path.join('img_result', str(unix_time), '0.jpg')
        # print(result_path)
        return render_template('upload2.html', form=form, new_filename=new_filename, result_img=result_path)
    return render_template('upload2.html', form=form)


@main.route('/', )
@main.route('/index/', )
def index():
    return render_template('index.html', )


@main.route('/user/')
def user():
    pass


@main.route('/moderate/')
def moderate():
    pass



