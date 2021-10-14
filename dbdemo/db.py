import os
import sqlite3
import json


# From: https://goo.gl/YzypOI


def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


class DatabaseDriver(object):
    """
    Database driver for the Task app.
    Handles with reading and writing data with the database.
    """

    def __init__(self):
        self.conn = sqlite3.connect("tasks.db", check_same_thread=False)
        self.create_tasks_table()

    def create_tasks_table(self):
        try:
            self.conn.execute("""
                CREATE TABLE tasks(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    done BOOLEAN NOT NULL
                );
            """)
        except Exception as e:
            print(e)

    def get_task_by_id(self, id):
        cursor = self.conn.execute("SELECT * FROM tasks WHERE id= ?; ", (id,))
        for row in cursor:
            return {"id": row[0], "description:": row[1], "done": bool(row[2])}
        return None

    def get_tasks(self):
        cursor = self.conn.execute("SELECT * FROM tasks;")
        tasks = []
        for row in cursor:
            tasks.append(
                {"id": row[0], "description": row[1], "done": bool(row[2])})
        return tasks

    def create_task(self, description, done):
        cursor = self.conn.cursor()
        cursor.execture("""
            INSERT INTO tasks(description, done) VALUES (?, ?);
        """, (description, done))
        self.conn.commit()
        return cursor.lastrowid

    def update_task(self, task_id, descritpion, done):
        self.conn.execute("""
                          UPDATE tasks SET descritpion = ?, done = ? WHERE id = ?;
                          """, (descritpion, done, task_id))
        self.conn.commit()

    def delete_task(self, task_id):
        self.conn.execute("DELETE FROM tasks WHERE id = ?;", (task_id))
        self.conn.commit()


        # Only <=1 instance of the database driver
        # exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)
