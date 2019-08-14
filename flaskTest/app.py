'''
@Description: 主页
@Author: lkb
@Date: 2019-08-08 14:48:10
@LastEditTime: 2019-08-14 19:51:25
@LastEditors: Please set LastEditors
'''
from flask import render_template, request, session, redirect, url_for, make_response
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import json
import pymysql
import os
import myFunc as myFunc
import config
from config import app

# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])

'''
@description: 登录页路由
@param {type} 
@return: 登录页面
'''
@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if session.get('username'):
        redirect('/user')
    return render_template('login.html')

'''
@description: 注册页路由
@param {type} 
@return: 注册页面
'''
@app.route('/regist')
def regist():
    return render_template('regist.html')

'''
@description: 提交登录表单
@param {type} 
@return: 是否成功登录
'''
@app.route('/loginForm', methods=['POST'])
def loginForm():
    print(request.form['username'])
    print(request.form['password'])
    if(myFunc.canLogin(request.form)):
        session.permanent = True
        app.permanent_session_lifetime = timedelta(seconds=600)
        session['username'] = request.form['username']
        # session['isOnline'] = True
        # return redirect(url_for('user', username = session['username']))
        result = {
            "wrong": False,
            "url": url_for('user', username=session['username'])
        }
        print(result)
        return json.dumps(result)
    else:
        result = {
            "wrong": True
        }
        return json.dumps(result)

'''
@description: 提交注册表单
@param {type} 
@return: 是否注册成功
'''
@app.route('/registForm', methods=['POST'])
def registForm():
    # print(request.form)
    data = {
        "username": request.form['username'],
        "password": request.form['password']
    }
    print(data)
    if myFunc.canRegist(data):
        success = myFunc.regist(data)  # 记录是否成功插入
        print(success)
        if success:
            result = {
                'success': True,
                'error': False
            }
        else:
            result = {
                'success': True,
                'error': True
            }
    else:
        result = {
            'success': False,
            'error': '已有相同用户名'
        }
    return json.dumps(result)

'''
@description: 提交图片路由
@param {type} 
@return: 处理后的结果图片
'''
@app.route('/uploadImage', methods=['POST'])
def uploadimage():
    pic = request.files.get('pic')
    print(pic)
    print(type(pic))
    # 对图片重命名
    # 对图像进行处理
    # 记获得的图片为pic
    basedir = os.path.abspath(os.path.dirname(__file__))
    # print(pic)
    path = basedir+"/static/photos/"+pic.filename
    pic.save(path)
    print(path)
    result = {
        'success': True,
        # 'data' : data
        'url': "../static/photos/"+pic.filename
    }

    return json.dumps(result)

'''
@description: 用户页路由
@param {type} 
@return:   用户页
'''
@app.route('/user', methods=['GET'])
def user():
    if session.get('username') is None:
        return redirect('/login')
    return render_template('user.html')

'''
@description: 注销页路由
@param {type} 
@return: 注销页面
'''    
@app.route('/logout')
def logout():
    session.pop('username',None)
    return 'yes'

'''
@description: 忘记密码页
@param {type} 
@return: 忘记密码页面
'''    
@app.route('/forgetPass')
def forgetPass():
    return render_template('forgetPass.html')


# @app.route('/photos/<string:filename>', methods=['GET'])
# def showPhoto(filename):
#     if(filename is None):
#         pass
#     else:
#         path = os.path.abspath(os.path.dirname(__file__)) + \
#             "/static/photos/"+filename
#         print(path)
#         image_data = open(path)
#         response = make_response(image_data)
#         response.headers['Content-Type'] = 'image/png'
#         return response

'''
@description: 主函数
@param {type} 
@return: 
'''
if __name__ == '__main__':
    app.run()
