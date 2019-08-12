import os
basedir = os.path.abspath(os.path.dirname(__file__))


#
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SSL_REDIRECT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30
    FLASKY_SLOW_DB_QUERY_TIME = 0.5

    @staticmethod
    def init_app(app):
        pass


class TestingConfig(Config):
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'tests', 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'tests', 'db_repository')

    # 上传的图片的保存路径
    IMG_DIR = os.path.join(basedir, 'app', 'static', 'img_upload')  # 只能存在static下吗？
    # 指尖模型所在路径
    MODEL_PATH = '/home/wen/PycharmProjects/test00_1/Fingers_200W/output_graph/frozen_inference_graph.pb'
    # 切割子图与框底边（即指尖位置）的上距离与下距离
    TOP_B = 10
    BOTTOM_B = 30
    LEFT_B = 0
    RIGHT_B = 0
    # 保存结果的路径
    RESULT_DIR = os.path.join(basedir, 'app', 'static', 'img_result')

    HOST = "0.0.0.0"
    PORT = 5000


config = {
    'testing': TestingConfig,

    'default': Config
}
