from typing import Any
from roombot.types.datatypes import User


class IUsersTable:
    async def get_user_by_id(self, user_id: int) -> User or None: ...
    async def get_user_by_telegram_id(self, telegram_id: int) -> User or None: ...
    # ADD
    async def add_user(self, user: User) -> User: ...
    # SET
    async def edit_user_data(self, user: User) -> Any: ...
    async def set_user_room_by_id(self, user_id: int, room: str) -> bool: ...
    async def set_user_room_by_telegram_id(self, telegram_id: int, room: str) -> bool: ...
    async def set_user_permission_by_telegram_id(self, telegram_id: int, permission: str) -> bool: ...