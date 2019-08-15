from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Picture, Permission
from .decorators import permission_required
from . import api
from .errors import forbidden


@api.route('/picture/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/posts/<int:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route('/posts/', methods=['POST'])
@permission_required(Permission.UPLOAD)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, \
        {'Location': url_for('api.get_post', id=post.id)}



ALLOWED_EXTENSIONS = set(['png', 'jpg'])
# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 上传文件
@main.route('/detection_old/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def detection_old():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        file_dir = current_app.config['IMG_DIR']
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        f = request.files['img']  # 从表单的file字段获取文件，myfile为该表单的name值
        # print(f.filename)
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