import databases
import sqlalchemy

from roombot.interfaces.IUsersTable import IUsersTable
from roombot.types.datatypes import User
from roombot.utils.database import AutoCreateTables
from .default_tables import users as default_users_columns
from typing import List


class PostgreSQLUsers(IUsersTable, AutoCreateTables):
    def __init__(self, database: databases.Database, additional_columns: List[sqlalchemy.Column] = None):
        if not additional_columns:
            additional_columns = []

        self.metadata = sqlalchemy.MetaData()
        self.database = database
        self.users_table = sqlalchemy.Table(
                        "users",
                        self.metadata,
                        *default_users_columns,
                        *additional_columns
        )
        self.init_users_table(default_users_columns, additional_columns)

    async def add_user(self, user: User) -> User:
        query1 = (
            self.users_table.insert()
            .values(**user.as_dict())
            .returning(self.users_table.c.id)
        )
        query2 = (
            self.users_table.select()
            .where(self.users_table.c.telegram_id == user.telegram_id)
        )

        uid = await self.database.fetch_one(query2)
        if uid:
            user.id = uid.get("id")
            return user
        user.id = (await self.database.fetch_one(query1)).get("id")
        return user

    async def get_user_by_id(self, user_id: int) -> (User or None):
        query = (
            self.users_table.select()
            .where(self.users_table.c.id == user_id)
        )
        result = await self.database.fetch_one(query)
        if result:
            user = User(**result)
            return user
        return None

    async def get_user_by_telegram_id(self, telegram_id: int) -> (User or None):
        query = (
            self.users_table.select()
            .where(self.users_table.c.telegram_id == telegram_id)
        )
        result = await self.database.fetch_one(query)
        if result:
            user = User(**result)
            return user
        return None

    async def set_user_room_by_id(self, user_id: int, room: str) -> bool:
        query = (
            self.users_table.update()
            .where(self.users_table.c.id == user_id)
            .values(room=room)
        )
        await self.database.execute(query)
        return True

    async def set_user_room_by_telegram_id(self, telegram_id: int, room: str) -> bool:
        query = (
            self.users_table.update()
            .where(self.users_table.c.telegram_id == telegram_id)
            .values(room=room)
        )
        await self.database.execute(query)
        return True

    async def set_user_permission_by_telegram_id(self, telegram_id: int, permission: str) -> bool:
        query = (
            self.users_table.update()
            .where(self.users_table.c.telegram_id == telegram_id)
            .values(permissions=permission)
        )
        await self.database.execute(query)
        return True
