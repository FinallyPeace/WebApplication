import os, time
from flask import Flask, render_template, session, request, make_response, redirect, url_for
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
# app.SECRET_KEY = os.urandom(24)

# cookie
@app.route('/setCookie', methods=['GET', 'POST'])
def setCookie():
    if request.method == 'POST':
        user = request.form['userID']
    response = make_response(render_template('read-cookie.html', userID=user))
    response.set_cookie('userID', user)
    
    return response

@app.route('/getCookie')
def getCookie():
    user = request.cookies.get('userID')
    return f'cookie with name "userID" is "{user}"'

# session
# @app.route('/getSession')
# def getSession():
#     name = session.get('name')
#     return f'session with name "name" is "{name}"'

# @app.route('/setSession')
# def setSession():
#     name = 'KID
#     session['name'] = name
#     return f'session with name "name" is set to "{name}"'

@app.route('/')
def form():
    if 'userID' in session:
        userID = session['userID']
        return '登入名稱:' + userID + "<br><b><a href='/logout'>點此登出</a></b>"
    return "您尚未登入<br><a href='/login'>點此登入</a>"

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['userID'] = request.form['userID']
        return redirect(url_for('form'))
    print(session)
    return render_template('form.html')

@app.route('/logout')
def logout():
    session.pop('userID', None)
    print(session)
    return redirect(url_for('form'))

# @app.route('/log-in')
# def log_in():
#     return render_template('log-in.html')

# @app.route('/log-in', methods = ["GET", "POST"])
# def verify():
#     if request.method == 'POST':
#         if request.form.get('name') == 'admin':
#             return redirect(url_for('success'))
#         else:
#             abort(401)
#     else:
#         return redirect(url_for('log_in'))

# @app.route('/success')
# def success():
#     return "登入成功"