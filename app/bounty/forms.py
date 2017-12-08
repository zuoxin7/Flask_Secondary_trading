from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, Bountyissue

class BountyForm(FlaskForm):
    name = StringField('目标名称',
                        validators=[Required(), Length(1, 64),])
    introduction = TextAreaField('目标细节')
    price = StringField('悬赏金(平台将扣取5%的佣金)')
    image = FileField('请上传目标图片(jpg、png、jpeg)',
                      validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], '只允许上传图片!')])
    submit = SubmitField('发布')

class BountyComment(FlaskForm):
    bounty_comment = TextAreaField('悬赏回馈')
    submit = SubmitField('提交')