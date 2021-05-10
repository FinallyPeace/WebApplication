import json
from flask import Flask, render_template, request , jsonify
app = Flask(__name__)

@app.route("/")
def template():
    return render_template('template.html')

# @app.route("/")
# @app.route("/<name>")
# def hello(name = None):
#     if name == None:
#         return "<h1 style='color:red;'>首頁</h1>"
#     return "<h1>第二層 <span style='color:blue;'>"+ name + "</span></h1>"

# 取得網址 Query 資料的方法
# addr: /query?name=xxx&age=25
# @app.route("/query")
# def query():
#     name = request.args.get('name')
#     age = request.args.get('age')
#     return f'Name:{name}, Age:{age}'

# 取得表單資料的方法 form-data
# @app.route('/form')
# def form():
#     return render_template('form.html')
# # request.form.get == request.values.get
# @app.route("/process", methods=['POST'])
# def post_form():
#     result = request.values.to_dict()
#     return json.dumps(result, ensure_ascii=False)

# 直接將 dict 轉為 JSON
# @app.route('/json', methods=['GET', 'POST'])
# def json():
#     name = request.args.get('name')
#     return jsonify({
#         'name': name
#     })

tasks = {
    0:{
        'id':0,
        'description':'todo-1',
        'done':False
    },
    1:{
        'id':1,
        'description':'todo-2',
        'done':False
    }
}
task_id_counter = 2

@app.route('/tasks')
def get_tasks():
    response = {
        'success':True,
        'data':list(tasks.values())
    }
    return jsonify(response)

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    # 將取得的資料以 json 載入 (將已編碼的 JSON 字串解碼為 Python 物件)
    body = json.loads(request.data)
    # 指定拿取 description , 若無則顯示 no description
    description = body.get('description', 'no description')

    task = {
        'id':task_id_counter,
        'description':description,
        'done':False
    }

    tasks[task_id_counter] = task
    task_id_counter += 1
    # 將 Python 物件編碼成 JSON 字串
    return json.dumps({
        'success':True,
        'data':task
    }), 201

@app.route('/tasks/<int:task_id>')
def get_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return json.dumps({
            'success':False,
            'error':'Task not found'
        }), 404
    return json.dumps({
        'success':True,
        'data':task
    }), 200

@app.route('/tasks/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return json.dumps({
            'success':False,
            'error':'Task not found'
        }), 404
    body = json.loads(request.data)
    description = body.get('description')
    if description:
        task['description'] = description
    task['done'] = body.get('done', False)
    return json.dumps({
        'success':True,
        'data':task
    }), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return json.dumps({
            'success':False,
            'error':'Task not found'
        }), 404
    del tasks[task_id]
    return json.dumps({
        'success':True,
        'data':task
    }), 200

