# from flaskr import view 需在初始化下方，不可使用自動排版
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# 返回絕對路徑
pjdir = os.path.abspath(os.path.dirname(__file__))

# 專案環境變數
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(pjdir, 'data.sqlite')
app.config['SECRET_KEY'] = os.urandom(24)

SESSION_PROTECTION = 'strong'

# 套件參數初始化
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login = LoginManager(app)
login.login_view = 'login'

#  載入專案中的route頁面
from flaskr import view