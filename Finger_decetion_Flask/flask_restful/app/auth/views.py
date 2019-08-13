from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User
from .forms import LoginForm


@auth.route('/login/', methods=['GET', 'POST'], )
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            # Flask_Login 把原URL保存在查询字符串的next参数中
            next = request.args.get('next')
            # 防止恶意攻击，确保相对路径
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


# login_required 确保用户是已经授权的用户
@auth.route('/logout/', )
@login_required
def logout():
    logout_user()
    flash('You have been logged out!')
    return redirect(url_for('main.index'))






