from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, GoodsissueGoods

class GoodsForm(FlaskForm):
    name = StringField('商品名称',
                        validators=[Required(), Length(1, 64),])
    introduction = TextAreaField('商品介绍')
    category = SelectField('商品类别', choices=[('learn', '学习类'), ('life', '生活类')])
    price = StringField('价格(平台将扣除5%的佣金)')
    image = FileField('请上传你的图片(jpg、png、jpeg)', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('发布')

class GoodComment(FlaskForm):
    good_comment = TextAreaField('商品回馈')
    submit = SubmitField('提交')