import sqlite3
import json
from roombot.interfaces.IDatabase import IDatabase
from .sqlite_users import Sqlite3Users
from typing import Any


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Sqlite3Database(IDatabase):
    conn: sqlite3.Connection = None
    cursor: sqlite3.Cursor = None
    users: Sqlite3Users
    filename: str

    def __init__(self, filename: str):
        self.users = Sqlite3Users(self)
        self.filename = filename

    def connect(self):
        self.conn = sqlite3.connect(self.filename)
        self.conn.row_factory = dict_factory
        self.cursor = self.conn.cursor()

    def execute(self, request, arguments: list = None) -> Any:
        if self.cursor:
            self.cursor.execute(request, arguments)
            return self.cursor.fetchall()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
