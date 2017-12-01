from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required


class PostForm(FlaskForm):
    body = TextAreaField("你想要发布什么信息？", validators=[Required()])
    submit = SubmitField('Submit')