from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, GoodsissueGoods

class GoodsForm(FlaskForm):
    name = StringField('商品名称',
                        validators=[Required(), Length(1, 64),])
