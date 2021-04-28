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
    app.logger.info(request)
    if request.method == 'POST':
        # 連接資料庫檔案
        con = sql.connect('database.db')
        msg = "新增失敗"
        try:
            name = request.form['name']
            city = request.form['city']
            pin = request.form['pin']
            addr = request.form['addr']

            name = name if len(name) else None
            print("name:", name)
            if name is None:
                raise Exception("名字 不可為空")

            if int(pin) < 0:
                print("pinCode:", pin)
                raise Exception("PinCode 不可為負數")
            # 傳回 Cursor物件 (Cursor 為資料庫指標)
            cursor = con.cursor()
            # 執行SQL指令
            cursor.execute("INSERT INTO students(name, city, pin, addr) VALUES(?, ?, ?, ?)", (name, city, pin, addr))
            # 將之前的操作變更到資料庫
            con.commit()
            msg = '新增成功'
        except Exception as e:
            app.logger.error(e)
            # 取消最近的commit()變更，回復到之前狀態
            con.rollback()
        finally:
            con.close()
            return render_template('result.html', msg=msg)

@app.route('/list')
def list():
    with sql.connect('database.db') as con:
        # 更改回傳型態，預設為tuple
        con.row_factory = sql.Row

        cursor = con.cursor()
        cursor.execute("SELECT * FROM students")
        # 讀取全部剩餘的紀錄以串列回傳，若無紀錄回傳空串列
        # fetchone() -> 讀取目前cursor所指的下一筆紀錄，若無回傳None
        rows = cursor.fetchall()

    return render_template("list.html", rows=rows)
