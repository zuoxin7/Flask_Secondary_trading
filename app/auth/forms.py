from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('保持登录状态')
    submit = SubmitField('登陆')


class RegistrationForm(FlaskForm):
    email = StringField('邮箱',
                        validators=[Required(), Length(1, 64),
                                    Email()])

    username = StringField('用户名',
                           validators=[Required(),
                                       Length(1, 64),
                                       Regexp('^[A-Za-z0-9_.]*$', 0,
                                              '用户名只允许为字母、数字、点和下划线 ')])
    password = PasswordField(
        '密码',
        validators=[Required(),
                    EqualTo('password2', message='俩次密码不一致')])
    password2 = PasswordField('确认密码', validators=[Required()])
    phone = StringField('电话', validators=[Required(),
                                            Regexp('^[1]{1}[0-9]{10}', 0,
                                                   '请输入正确的电话号码')])
    pay = StringField('支付宝账号', validators=[Required(), Length(1, 64)] )
    grade = StringField('年级*')
    academy = StringField('学院*')
    major = StringField('专业*')
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.select().where(User.email == field.data).first():
            raise ValidationError('邮箱已经存在')

    def validate_username(self, field):
        if User.select().where(User.username == field.data).first():
            raise ValidationError('用户名已经存在')
