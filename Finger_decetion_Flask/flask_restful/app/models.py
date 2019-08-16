from app import db
from .exceptions import ValidationError
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import login_manager


# flask_login要求 获取指定标志符对应的用户时调用
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Permission:
    UPLOAD = 1
    # ...
    ADMIN = 16


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)  # 权限
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permission(self, ):
        self.permissions = 0

    # 角色    权限
    # 管理员   ...
    # 用户    ...
    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.UPLOAD, ],
            'Administrator': [Permission.UPLOAD, ]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % (self.permissions)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128), )
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    picture = db.relationship('Picture', backref='user', lazy='dynamic')

    # 定义默认用户角色
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            # 有BUG，没能默认管理员
            # if self.email == current_app.config['FLASKY_ADMIN']:
            #     self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    # 权限控制
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    # 序列化json
    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id),
            'nickname': self.nickname,
            'pic_count': self.picture.count(),
        }
        return json_user

    # 密码属性
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 支持令牌的身份验证
    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id}).edcode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % (self.nickname)


# 为了can方法和is_administrator方法使用方便
class AnonymousUser(AnonymousUserMixin):
    def can(self, permission):
        return False

    def is_administrator(self):
        return False


class Picture(db.Model):
    __tablename__ = 'pictures'
    id = db.Column(db.Integer, primary_key=True)
    pic_name = db.Column(db.String(120))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 表名.id

    # 序列化为json格式字典
    def to_json(self):
        json_pic = {
            'url': url_for('api.get_pic', id=self.id),
            'user_url': url_for('api.get_user', id=self.user_id),
            'pic_name': self.pic_name,
        }
        return json_pic

    # 反序列化
    @staticmethod
    def from_json(json_pic):
        # 关靠名字可能没什么用，要改的
        pic_name = json_pic.get('pic_name')
        if pic_name is None or pic_name == '':
            raise ValidationError('dose not have picture name')
        return Picture(pic_name=pic_name)

    def __repr__(self):
        return '<Picture: %r>' % (self.pic_name)

