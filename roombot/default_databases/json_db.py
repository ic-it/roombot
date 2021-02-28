import sqlite3
import json
from roombot.interfaces.IDatabase import IDatabase
from .json_users import JsonUsersTable
from typing import Any


class JsonDatabase(IDatabase):
    conn: dict
    users: JsonUsersTable
    filename: str

    def __init__(self, filename: str):
        self.filename = filename
        self.users = JsonUsersTable(self)

    def connect(self):
        self.conn = json.load(open(self.filename, "r"))

    def execute(self, request, arguments: list = None) -> Any:
        pass

    def commit(self):
        json.dump(self.conn, open(self.filename, "w"))

    def close(self):
        self.commit()
