from flask import Flask, render_template
import os
# 載入資料庫操作
from model import db, UserRegister
# 載入bootstrap
from flask_bootstrap import Bootstrap
# 載入表單
from form import FormRegister

app = Flask(__name__, template_folder='./template')


# 在路由檔案中設定起始參數
pjdir = os.path.abspath(os.path.dirname(__file__))
#  新版本的部份預設為none，會有異常，再設置True即可。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#  設置資料庫為sqlite3
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(pjdir, 'data_register.sqlite')
app.config['SECRET_KEY'] = os.urandom(24)

db.init_app(app)
with app.app_context():
    db.create_all()

# 表單初始化(附加在初始化區段下方)
bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def register():
    form = FormRegister()
    if form.validate_on_submit():
        user = UserRegister(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        return '註冊成功！'
    return render_template('register.html', form=form)
