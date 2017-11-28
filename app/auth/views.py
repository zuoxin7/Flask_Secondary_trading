from flask import render_template, redirect, request, url_for, flash, session
from flask import make_response
from flask_login import login_user, logout_user, login_required

from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.select().where(User.email == form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            response=make_response()
            username=User.select().where(User.email == form.email.data).first().username
            response.set_cookie('username',username)
            # return redirect(request.args.get('next') or url_for('main.index', name=User.select().where(User.email == form.email.data).first().username)) and response
            return response and redirect(url_for('main.index'))
        flash('用户名或密码输入错误')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经退出')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    phone=form.phone.data,
                    pay=form.pay.data,
                    academy=form.academy.data,
                    grade=form.grade.data,
                    major=form.major.data)
        user.save()
        flash('你现在可以登录了')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
