from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# 建立關聯資料關係
association_table = db.Table(
    'association',
    db.Column('task_id', db.Integer, db.ForeignKey('task.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
)


class Task(db.Model):
    __tablename__ = 'task'		# table 代稱
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)

    # 建立關聯
    subtasks = db.relationship('Subtask', cascade='delete')
    categories = db.relationship('Category', secondary=association_table, back_populates='tasks')

    def __init__(self, **kwargs):
        self.description = kwargs.get('description')
        self.done = kwargs.get('done')

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "done": self.done,
            # 在 Task 加入取值剖析
            "subtasks": [s.serialize() for s in self.subtasks],
            "categories": [c.serialize() for c in self.categories]
        }


class Subtask(db.Model):
    __tablename__ = 'subtask'  # table 代稱
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    done = db.Column(db.Boolean, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

    def __init__(self, **kwargs):
        self.description = kwargs.get('description')
        self.done = kwargs.get('done')
        self.task_id = kwargs.get('task_id')

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "done": self.done}


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False)

    # 在Category 建立關係
    tasks = db.relationship(
        'Task', secondary=association_table, back_populates='categories')

    def __init__(self, **kwargs):
        self.description = kwargs.get('description')
        self.color = kwargs.get('color')

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "color": self.color}
