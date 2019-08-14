from hello import User,db
from sqlalchemy.sql import func
db.create_all()
# db.drop_all()
# db.session.add(Role(name = 'Admin'))
# db.session.add(Role(name = 'User'))
# db.session.commit()
# print(Role.query.filter_by(name = 'Admin').first())
# print(Role.query.with_entities(func.sum(Role.id)).all())
