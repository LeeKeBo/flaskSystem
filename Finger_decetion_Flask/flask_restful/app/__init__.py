from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # 蓝本注册
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')  # 该蓝本下的路由都会附加/auth前缀

    # from .api import api as api_blueprint
    # app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app


# 避免import冲突
import os
from migrate.versioning import api


def create_db(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    db.app = app
    db.create_all()

    if not os.path.exists(app.config['SQLALCHEMY_MIGRATE_REPO']):
        api.create(app.config['SQLALCHEMY_MIGRATE_REPO'], 'database repository')
        api.version_control(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO'])
    else:
        api.version_control(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO'],
                            api.version(app.config['SQLALCHEMY_MIGRATE_REPO']))


