import sqlite3


class DatabaseDriver(object):
    """
    Database driver for the Venmo (Full) app.
    Handles with reading and writing data with the database.
    """

    def __init__(self):
        self.conn = sqlite3.connect("user.db", check_same_thread=False)
        self.create_task_table()
