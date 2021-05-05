import json
from flask import Flask, request
from db import db
from db import Task, Subtask, Category

# 定義db 名稱
db_filename = "todo.db"
app = Flask(__name__)

# 設定 db config
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_filename}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

# 初始化
db.init_app(app)
with app.app_context():
    db.create_all()

# reponse format


def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code


def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code


@app.route("/")
@app.route("/tasks")
def get_tasks():
    tasks = [t.serialize() for t in Task.query.all()]
    return success_response(tasks)


@app.route("/subtasks")
def get_subtasks():
    subtasks = [s.serialize() for s in Subtask.query.all()]
    return success_response(subtasks)


@app.route("/categories")
def categories():
    categories = [c.serialize() for c in Category.query.all()]
    return success_response(categories)


@app.route("/tasks", methods=["POST"])
def create_task():
    body = json.loads(request.data)

    new_task = Task(
        description=body['description'],
        done=body.get('done', False)
        # 無法取得數值時，給予初始值避免出錯
    )

    db.session.add(new_task)
    db.session.commit()
    return success_response(new_task.serialize(), 201)


@app.route("/tasks/<int:task_id>")
def get_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    # first() 取出查詢到的第一行資料

    # 下面檢查是否沒有取得任何內容
    if task is None:
        return failure_response("Task not found!")
    return success_response(task.serialize())


@app.route("/tasks/<int:task_id>", methods=["POST"])
def update_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return failure_response("Task not found!")

    # 取得新輸入的值
    body = json.loads(request.data)
    task.description = body.get('description', task.description)
    task.done = body.get('done', task.done)

    db.session.commit()
    return success_response(task.serialize())


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return failure_response("Task not found!")

    db.session.delete(task)
    db.session.commit()
    return success_response(task.serialize())


@app.route("/tasks/<int:task_id>/subtasks", methods=["POST"])
def create_subtask(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return failure_response("Task not found!")

    body = json.loads(request.data)
    new_subtask = Subtask(
        description=body.get('description'),
        done=body.get('done'),
        task_id=task_id
    )

    db.session.add(new_subtask)
    db.session.commit()
    return success_response(new_subtask.serialize())


@app.route("/tasks/<int:task_id>/category", methods=["POST"])
def assign_category(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return failure_response("Task not found!")

    body = json.loads(request.data)
    description = body.get('description')
    if description is None:
        return failure_response("No description!")

    category = Category.query.filter_by(description=description).first()
    if category is None:
        category = Category(
            description=description,
            color=body.get('color', 'purple')
        )

    task.categories.append(category)
    db.session.commit()
    return success_response(task.serialize())
