from config import app
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, nullable=False,
                   primary_key=True, autoincrement=True)
    # role_id = db.Column(db.Integer,nullable = False,unique = True)
    name = db.Column(db.String(30),nullable=False,unique = True)
    password = db.Column(db.String(50),nullable = False)
    def __repr__(self):
        return '<User %r>' % self.name

        

# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, nullable=False,
#                    primary_key=True, autoincrement=True)
#     name = db.Column(db.String(16), nullable=False,
#                      server_default='', unique=True)

#     def __repr__(self):
#         return '<Role %r>' % self.name


# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, nullable=False,
#                    primary_key=True, autoincrement=True)
#     username = db.Column(db.String(32), nullable=False,
#                          unique=True, server_default='', index=True)
#     role_id = db.Column(db.Integer, nullable=False, server_default='0')

#     def __repr__(self):
#         return '<User %r,Role id %r>' % (self.username, self.role_id)
