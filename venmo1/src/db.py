import os
import sqlite3

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
        self.conn = sqlite3.connect("venmo.db", check_same_thread=False)
        self.create_user_table()

    def create_user_table(self):
        try:
            self.conn.execute("""
                CREATE TABLE user(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    NAME TEXT NOT NULL
                    USERNAME TEXT NOT NULL,
                    BALANCE
                );
                """)
        except Exception as e:
            print(e)

    def get_all_users(self):
        cursor = self.conn.execute("SELECT * FROM user;")
        users = []

        for row in cursor:
            users.append({"id": row[0], "name": row[1],
                         "username": row[2], "balance": row[3]})

        return users

    def get_all_users_secure(self):
        cursor = self.conn.execute("SELECT * FROM user;")
        users = []

        for row in cursor:
            users.append({"id": row[0], "name": row[1],
                         "username": row[2]})

        res = {"users": users}
        return res

    def insert_user_table(self, name, username, balance):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO user (NAME, USERNAME, BALANCE) VALUES (?, ?, ?);", (name, username, balance))
        self.conn.commit()
        return cursor.lastrowid

    def get_user_by_id(self, id):
        cursor = self.conn.execute("SELECT * FROM user WHERE ID = ?", (id, ))

        for row in cursor:
            return {"id": row[0], "name": row[1], "username": row[2], "balance": row[3]}

        return None

    def get_sender_balance(self, sender_id):
        cursor = self.conn.execute(
            "SELECT balance FROM user WHERE ID = ?", (sender_id,))

        for row in cursor:
            return {"balance": row[0]}
        return None

    def delete_user_by_id(self, id):
        self.conn.execute("""
                          DELETE FROM user
                          WHERE id = ?;
                          """, (id,))
        self.conn.commit()

    def send_money(self, sender_id, receiver_id, amount):

        # if (sender_balance < amount):
        #     return failure_response("Insufficient funds", 400)

        self.conn.execute("""
            UPDATE user
            SET balance = balance - ?
            WHERE id = ?;
        """, (amount, sender_id))
        self.conn.execute("""
            UPDATE user
            SET balance = balance + ?
            WHERE id = ?;
        """, (amount, receiver_id))
        self.conn.commit()
        res = {
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "amount": amount}
        # return success_response(res)
