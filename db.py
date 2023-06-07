import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

    def task_exists(self, task_id):
        with self.connection:
            result = self.cursor.execute("SELECT task FROM tasks WHERE id = ?", (task_id,)).fetchone()
            if result is None:
                return False
            else:
                return True

    def is_user_task(self, user_id, task_id):
        with self.connection:
            result = self.cursor.execute("SELECT user_id FROM tasks WHERE id = ?", (task_id,)).fetchone()
            if int(result[0]) == int(user_id):
                return True
            else:
                return False

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))

    def add_task(self, user_id, user_task):
        with self.connection:
            return self.cursor.execute("INSERT INTO tasks (user_id, task) VALUES ('%s', '%s')" % (user_id, user_task,))

    def get_tasks(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,)).fetchall()
            return result

    async def set_task(self, task_id, task_datatime):
        with self.connection:
            return self.cursor.execute('UPDATE tasks SET task_datatime = ? WHERE id = ?', (task_datatime, task_id,))

    async def edit_task(self, task_id, user_task, task_datatime):
        with self.connection:
            task_status = "not complete"
            return self.cursor.execute('UPDATE tasks SET task = ?, task_datatime = ?, status = ? WHERE id = ?',
                                       (user_task, task_datatime, task_status, task_id,))

    async def get_task(self, task_id):
        with self.connection:
            result = self.cursor.execute("SELECT task FROM tasks WHERE id = ?", (task_id,)).fetchone()
            return result[0]

    async def get_time(self, task_id):
        with self.connection:
            result = self.cursor.execute("SELECT task_datatime FROM tasks WHERE id = ?", (task_id,)).fetchone()
            return result[0]

    async def set_status(self, task_id):
        with self.connection:
            task_status = "complete"
            return self.cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (task_status, task_id,))

    async def set_active(self, user_id):
        with self.connection:
            return self.cursor.execute('UPDATE users SET is_active = ? WHERE user_id = ?', (1, user_id,))

    async def is_active(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT is_active FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return result[0]
