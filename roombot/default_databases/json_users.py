from roombot.interfaces.IUsersTable import IUsersTable
from roombot.interfaces.IDatabase import IDatabase
from roombot.types.dataclasses import User


class JsonUsersTable(IUsersTable):
    database: IDatabase

    async def add_user(self, user: User) -> User:
        uid = len(self.database.conn.get("users"))
        user.id = uid
        self.database.conn["users"].append(user.as_dict())
        self.database.commit()
        return user

    async def get_user_by_id(self, user_id: int) -> (User or None):
        for usr in self.database.conn.get("users"):
            if usr.get("id") == user_id:
                return User(**usr)
        return None

    async def get_user_by_telegram_id(self, telegram_id: int) -> (User or None):
        for usr in self.database.conn.get("users"):
            if usr.get("telegram_id") == telegram_id:
                # print(usr)
                return User(**usr)
        return None

    async def set_user_room_by_id(self, user_id: int, room: str) -> bool:
        num = 0
        for usr in self.database.conn.get("users"):
            if usr.get("id") == user_id:
                self.database.conn["users"][num]["room"] = room
                self.database.commit()
                break
            num += 1
        return True

    async def set_user_room_by_telegram_id(self, telegram_id: int, room: str) -> bool:
        num = 0
        for usr in self.database.conn.get("users"):
            if usr.get("telegram_id") == telegram_id:
                self.database.conn["users"][num]["room"] = room
                self.database.commit()
                break
            num += 1
        return True

    async def set_user_permission_by_telegram_id(self, telegram_id: int, permission: str) -> bool:
        num = 0
        for usr in self.database.conn.get("users"):
            if usr.get("telegram_id") == telegram_id:
                self.database.conn["users"][num]["permissions"] = permission
                self.database.commit()
                break
            num += 1
        return True

