import sqlite3 as sql
from flask import Flask, render_template, request, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student')
def add_student():
    return render_template('student.html')

@app.route('/result', methods=['GET', 'POST'])
def addrec():
    if request.method == 'POST':
        try:
            name = request.form['name']
            city = request.form['city']
            pin = request.form['pin']
            addr = request.form['addr']

            with sql.connect("database.db") as con:
                cursor = con.cursor()
                cursor.execute("INSERT INTO students(name, city, pin, addr) VALUES(?, ?, ?, ?)", (name, city, pin, addr))

                con.commit()
                msg = '新增成功'
        except:
            con.rollback()
            msg = "新增失敗"
        finally:
            return render_template('result.html', msg=msg)
            con.close()

@app.route('/list')
def list():
    connect = sql.connect('database.db')
    connect.row_factory = sql.Row
    
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM students")

    rows = cursor.fetchall()
    return render_template("list.html", rows=rows)
