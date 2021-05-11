# flaskr 是專案裡的資料夾名稱
from flaskr import app
from flaskr import db
from flask import render_template, flash, redirect, url_for, request
from flaskr.model import UserRegister
from flaskr.form import FormRegister, FormLogin
from flask_login import login_user, current_user, login_required, logout_user


# db一樣要初始化
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
@login_required
def index():
    return render_template('base.html')


@app.route('/register', methods=['GET', 'POST'])
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


@app.route('/login')
def login():
    form = FormLogin()
    if form.validate_on_submit():
        user = UserRegister.query.fliter_by(email=form.email.data).first()
        if user:
            #  當使用者存在資料庫內再核對密碼是否正確。
            if user.check_password(form.password.data):
                login_user(user, form.remember_me.data)
                next = request.args.get('next')
                #  自定義一個驗證的function來確認使用者是否確實有該 url的權限
                if not next_is_valid(next):
                    return 'sorry!!'
                return redirect(next or url_for('index'))
            else:
                #  如果密碼驗證錯誤，就顯示錯誤訊息。
                flash('Wrong Email or Password')
        else:
            #  如果資料庫無此帳號，就顯示錯誤訊息。
            flash('Wrong Email or Password')
    return render_template('login.html', form=form)


def next_is_valid(url):
    return True


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('登出成功')
    return redirect(url_for('login'))


@app.route('/userinfo')
def userinfo():
    return 'Here is UserINFO'
