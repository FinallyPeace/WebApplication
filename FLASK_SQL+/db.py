import os
import sqlite3 as sql

class DatabaseDriver(object):
    def __init__(self):
        self.con = sql.connect('todo.db', check_same_thread = False)
        self.create_task_table()
        self.create_subtask_table()

    def create_task_table(self):
        try:
            self.con.execute(
                """
                CREATE TABLE task (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    done BOOLEAN NOT NULL
                );
                """
            )
        except Exception as e:
            print(e)

    def get_all_tasks(self):
        cursor = self.con.execute(
            """
            SELECT * FROM task;
            """
        )
        tasks = []
        for row in cursor:
            tasks.append({
                'id': row[0],
                'description': row[1],
                'done': row[2]
            })
        return tasks
    
    def insert_task_table(self, description, done):
        cursor = self.con.cursor()
        cursor.execute(
            """
            INiSERT INTO task (description, done) 
            VALUES (?, ?);
            """, (description, done))
        self.con.commit()
        # 顯示最後一筆id
        return cursor.lastrowid
    
    def get_task_by_id(self, id):
        cursor = self.con.execute("SELECT * FROM task WHERE ID = ?", (id,))

        for row in cursor:
            return {
                'id': row[0],
                'description': row[1],
                'done': row[2]
            }
        return None
    
    def update_task_by_id(self, id, description, done):
        self.con.execute(
            """
            UPDATE task
            SET description = ?, done = ?
            WHERE id = ?;
            """,
            (description, done, id),
        )
        self.con.commit()

    def delete_task_by_id(self, id):
        self.con.execute(
            """
            DELETE FROM task
            WHERE id = ?;
            """,
            (id,),
        )
        self.con.commit()

    # subtask
    def create_subtask_table(self):
        try:
            self.con.execute(
                """
                CREATE TABLE subtask (
                    id INTEGER PRIMARY KEY,
                    description TEXT NOT NULL,
                    done BOOL NOT NULL,
                    task_id INTEGER NOT NULL,
                    FOREIGN KEY(task_id) REFERENCES task(id)
                );
                """
            )
        except Exception as e:
           print(e)

    def insert_subtask(self, description, done, task_id):
        cursor = self.con.cursor()
        cursor.execute(
            """
            INSERT INTO subtask (description, done, task_id) 
            VALUES (?, ?, ?);
            """,(description, done, task_id)
        )
        self.con.commit()
        return cursor.lastrowid
    
    def get_subtasks_of_task(self, task_id):
        cursor = self.con.execute(
            """
            SELECT * FROM subtask WHERE task_id = ?
            """, (task_id,)
        )
        subtasks = []
        for row in cursor:
            subtasks.append({
                "id": row[0],
                "description": row[1],
                "done": bool(row[2])
            })
        return subtasks

    def get_subtasks_of_task(self, task_id):
        cursor = self.con.execute(
            """
            SELECT * FROM subtask WHERE task_id = ?
            """, (task_id,)
        )
        subtasks = []
        for row in cursor:
            subtasks.append({
                "id": row[0],
                "description": row[1],
                "done": bool(row[2])
            })
        return subtasks