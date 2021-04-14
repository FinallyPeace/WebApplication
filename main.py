from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)

# @app.route("/")
# @app.route("/<name>")
# def hello(name = None):
#     if name == None:
#         return "<h1 style='color:red;'>首頁</h1>"
#     return "<h1>第二層 <span style='color:blue;'>"+ name + "</span></h1>"

# @app.route('/hello/world', methods=['POST', 'GET'])
# def postGet():
#     return 'Post and Get'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/jp")
def jp():
    return render_template("jp.html")

@app.route("/test/<int:n>")
def num(n):
    return render_template("test.html", n=n)
