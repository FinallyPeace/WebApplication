from flask import Flask, render_template
import os
from view_form import UserForm
#  引入form類別
from flask_bootstrap import Bootstrap

app = Flask(__name__, template_folder='./template')
app.config['SECRET_KEY'] = os.urandom(24)
# flask_wtf 預設需要設置暗語，避免CSRF攻擊

bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def user():
    form = UserForm()
    #  flask_wtf 類中提供判斷是否表單提交過來的 method，不需要自行利用 request.method 來做判斷
    if form.validate_on_submit():
        return 'Success Submit'
    #  如果不是提交過來的表單，就是GET，這時候就回傳user.html網頁
    return render_template('user.html', form=form)
