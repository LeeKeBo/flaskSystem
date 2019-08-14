'''
@Description: 数据库功能测试
@Author: lkb
@Date: 2019-08-07 14:10:50
@LastEditTime: 2019-08-14 19:53:44
@LastEditors: 
'''
from dbModel import User,db
from sqlalchemy.sql import func
db.create_all()
# db.drop_all()
# db.session.add(Role(name = 'Admin'))
# db.session.add(Role(name = 'User'))
# db.session.commit()
# print(Role.query.filter_by(name = 'Admin').first())
# print(Role.query.with_entities(func.sum(Role.id)).all())
