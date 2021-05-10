#  載入flask_wtf
from flask_wtf import FlaskForm
#  各別載入需求欄位
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import EmailField
#  驗證方式
from wtforms.validators import DataRequired, Email

#  繼承 FlaskForm 開始


class UserForm(FlaskForm):
    username = StringField('使用者名稱', validators=[
                           DataRequired(message='Not Null')])
    email = EmailField('E-mail', validators=[DataRequired(message='Not Null')])
    submit = SubmitField('登入')
