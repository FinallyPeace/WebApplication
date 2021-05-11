from flaskr import app  # flaskr是專案裡的資料夾名稱
from flaskr import db
from flask import render_template
from flaskr.model import UserRegister
from flaskr.form import FormRegister

# db一樣要初始化
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return "This is index!"


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
