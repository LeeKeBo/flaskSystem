from app import create_db, create_app
from app.models import Role, User, db

if __name__ == '__main__':
    # create_db('testing')
    # Role.insert_roles()
    app = create_app('testing')
    db.init_app(app)
    db.app = app
    db.drop_all()
    db.create_all()  # 创建数据库以及建表，但是迁移时不可drop_all()又create_all()会丢失全部数据，这里暂且如此
    Role.insert_roles()
    user = User(nickname='JoJo', email='13798282351@qq.com', password='123456')
    db.session.add(user)
    db.session.commit()
    print(Role.query.all())
    Role.query.all()[0].add_permission(1)
    print(Role.query.all())
    print(User.query.all())
