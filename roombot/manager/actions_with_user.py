from roombot.types.dataclasses import User
from roombot.types.room import Room, RoomsStack
from roombot.interfaces.IUsersTable import IUsersTable


class ActionsWithUser:
    def __init__(self, users: IUsersTable, internal_data, rooms: RoomsStack):
        self.users = users
        self.internal_data = internal_data
        self.rooms = rooms

    async def go_to_room(self, user: User or int, room_name: str) -> int:
        if isinstance(user, int):
            user = await self.users.get_user_by_telegram_id(user)
            user: User

        if self.internal_data.users_migrations.get(user.telegram_id):
            return 2  # can't make recourse traveling

        for room in self.rooms.get(room_name):
            if self.user_can_go_to_room(user, room):
                self.internal_data.users_migrations[user.telegram_id] = room_name
                return 1  # can go
        return 0  # can't go

    async def set_permissions(self, user: User or int, permissions: str):
        if isinstance(user, User):
            await self.users.set_user_permission_by_telegram_id(user.telegram_id, permissions)
        elif isinstance(user, int):
            await self.users.set_user_permission_by_telegram_id(user, permissions)

    async def get_permissions(self, user: User or int):
        if isinstance(user, User):
            return (await self.users.get_user_by_telegram_id(user.telegram_id)).permissions
        elif isinstance(user, int):
            return (await self.users.get_user_by_telegram_id(user)).permissions

    def user_can_go_to_room(self, user: User, room: Room):
        myif = (user.permissions in room.permissions or ((user.permissions == self.internal_data.default_permissions or not len(user.permissions)) and not len(room.permissions))) or not len(room.permissions)
        if myif:
            return True
        return False

