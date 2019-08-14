'''
@Description: 数据库函数文件
@Author: lkb
@Date: 2019-08-08 15:19:05
@LastEditTime: 2019-08-14 19:56:21
@LastEditors: 
'''
from dbModel import User, db

'''
@description: 查询用户名与密码是否匹配
@param {type} 
@return: True or False
'''
def canLogin(data):
    user = User.query.filter(User.name == data['username'], User.password == data['password']).all()
    print(user)
    if user:
        return True
    return False

'''
@description: 判断是否能注册
@param {type} 
@return: True or False
'''    
def canRegist(data):
    user = User.query.filter(User.name == data['username']).all()
    if user:
        return False
    return True

'''
@description: 注册，数据库操作，并查询是否成功插入数据库
@param {type} 
@return: True or False
'''
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



    