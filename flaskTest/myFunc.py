from hello import User, db

# 注册
def loginIn(data):
    newUser = User(name=data['data'], password=data['password'],
                   role_id=data['role_id'])
    db.session.add(newUser)
    db.session.commit()
    

# 查询用户名与密码是否匹配
def canLogin(data):
    user = User.query.filter(User.name == data['username'], User.password == data['password']).all()
    print(user)
    if user:
        return True
    return False

def canRegist(data):
    user = User.query.filter(User.name == data['username']).all()
    if user:
        return False
    return True

def regist(data):
    print(data)
    db.session.add(User(name = data['username'],password = data['password']))
    db.session.commit()
    if canLogin(data):
        return True
    else:
        return False

# def findUser(username):
#     if(User.query.filter(User.name == username).first):
#         newUser = model.User(username,)
#         return newUser
#     return False



    