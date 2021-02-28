from roombot.interfaces.IUsersTable import IUsersTable
from roombot.types.dataclasses import User


class Sqlite3Users(IUsersTable):
    async def add_user(self, user: User) -> User:
        sql1 = """
        INSERT INTO users (telegram_id, firstname, lastname, permissions, room)
        VALUES (?, ?, ?, ?, ?);
        """
        sql2 = """
        SELECT id
        FROM users
        WHERE telegram_id = ?;"""
        uid = self.database.execute(sql2, [user.telegram_id, ])
        if uid:
            user.id = uid[0].get("id")
            return user
        self.database.execute(sql1, user.as_list())
        self.database.commit()
        uid = self.database.execute(sql2, [user.telegram_id, ])
        user.id = uid[0].get("id")
        return user

    async def get_user_by_id(self, user_id: int) -> (User or None):
        sql = """
                SELECT * 
                FROM users
                WHERE id = ?;"""
        result = self.database.execute(sql, [user_id, ])
        if result:
            user = User(**result[0])
            return user
        return None

    async def get_user_by_telegram_id(self, telegram_id: int) -> (User or None):
        sql = """
                SELECT * 
                FROM users
                WHERE telegram_id = ?;"""
        result = self.database.execute(sql, [telegram_id, ])
        if result:
            user = User(**result[0])
            return user
        return None

    async def set_user_room_by_id(self, user_id: int, room: str) -> bool:
        sql = """
                UPDATE users
                SET room = ?
                WHERE id = ?;"""
        self.database.execute(sql, [room, user_id])
        self.database.commit()
        return True

    async def set_user_room_by_telegram_id(self, telegram_id: int, room: str) -> bool:
        sql = """
                UPDATE users
                SET room = ?
                WHERE telegram_id = ?;"""
        self.database.execute(sql, [room, telegram_id])
        self.database.commit()
        return True

    async def set_user_permission_by_telegram_id(self, telegram_id: int, permission: str) -> bool:
        sql = """
                   UPDATE users
                   SET permissions = ?
                   WHERE telegram_id = ?;"""
        self.database.execute(sql, [permission, telegram_id])
        self.database.commit()
        return True

