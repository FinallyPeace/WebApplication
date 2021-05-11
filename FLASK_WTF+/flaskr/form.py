from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField, ValidationError, BooleanField
from wtforms.fields.html5 import EmailField
# 載入資料模型
from flaskr.model import UserRegister


class FormRegister(FlaskForm):
    """ 依照Model來建置相對應的Form  """
    username = StringField('使用者名稱', validators=[
        validators.DataRequired(),
        validators.Length(1, 30)
    ])
    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Length(1, 50),
        validators.Email()
    ])
    password = PasswordField('密碼', validators=[
        validators.DataRequired(),
        validators.Length(5, 10),
        validators.EqualTo('password2', message='密碼需要符合上欄輸入')
    ])
    password2 = PasswordField('密碼（請重複一次）', validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('建立帳號')

    # 在class FormRegister(Form)的最後加入
    def validate_email(self, field):
        if UserRegister.query.filter_by(email=field.data).first():
            raise ValidationError('信箱已被註冊')

    def validate_username(self, field):
        if UserRegister.query.filter_by(username=field.data).first():
            raise ValidationError('使用者名稱已被註冊')


class FormLogin(FlaskForm):
    """
    使用者登入使用，以email為主要登入帳號，密碼需做解碼驗證
    """
    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Length(1, 50),
        validators.Email()
    ])
    password = PasswordField('密碼', validators=[
        validators.DataRequired()
    ])
    remember_me = BooleanField('記住我')
    submit = SubmitField('登入')
