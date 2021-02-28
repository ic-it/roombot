import aiogram

from roombot.interfaces.ICallbackHandler import ICallbackHandler
from roombot.types.dataclasses import User
from roombot.types.handler import HandlersTypes
from roombot.interfaces.IUsersTable import IUsersTable
from roombot.types.room import Room
from roombot.utils.runfunc import run_func_as_async, get_kwargs_by_annotations, get_only_the_required_arguments


async def run_room_function(room: Room, callback: aiogram.types.CallbackQuery, internal_data, user: User):
    all_args = {aiogram.types.CallbackQuery: callback, User: user}
    all_args.update(internal_data.global_parameters)
    all_args.update(room.kwargs)
    args = get_kwargs_by_annotations(room.handler.function, all_args)
    args.update(get_only_the_required_arguments(room.handler.function, all_args))
    return await run_func_as_async(room.handler.function, **args)


class MainCallbackHandler(ICallbackHandler):
    def __init__(self, users: IUsersTable, rooms, internal_data, go_to_room):
        self.users = users
        self.rooms = rooms
        self.internal_data = internal_data
        self.go_to_room = go_to_room

    async def process_callback(self, callback: aiogram.types.CallbackQuery):
        user: User
        user_is_at_one_of_rooms: bool = False
        user = await self.users.get_user_by_telegram_id(callback.from_user.id)
        rooms = self.rooms.get(user.room, get_by_type=HandlersTypes.callback)
        if not rooms:
            return
        for room in rooms:
            user_is_at_one_of_rooms = True
            await run_room_function(room, callback, self.internal_data, user)
        if not user_is_at_one_of_rooms:
            await self.go_to_room(callback.from_user.id, self.internal_data.start_room)


class CheckUserCallbackHandler(ICallbackHandler):
    def __init__(self, users: IUsersTable, internal_data):
        self.users = users
        self.internal_data = internal_data

    async def process_callback(self, callback: aiogram.types.CallbackQuery):
        if not await self.users.get_user_by_telegram_id(callback.from_user.id):
            user_to_add = User(callback.from_user.id, callback.from_user.first_name, callback.from_user.last_name, self.internal_data.default_permissions, self.internal_data.start_room)
            await self.users.add_user(user_to_add)


class UserMigrationCallbackRoom(ICallbackHandler):
    def __init__(self, users: IUsersTable, rooms, internal_data, user_can_go_to_room):
        self.users = users
        self.rooms = rooms
        self.internal_data = internal_data
        self.user_can_go_to_room = user_can_go_to_room

    async def process_callback(self, callback: aiogram.types.CallbackQuery):
        user = await self.users.get_user_by_telegram_id(callback.from_user.id)
        user_migration = self.internal_data.users_migrations.get(user.telegram_id)
        if not user_migration: return
        on_join_callback_rooms = self.rooms.get(user_migration, get_by_type=HandlersTypes.on_join_callback) + self.rooms.get(user_migration, get_by_type=HandlersTypes.on_join_universal)
        if on_join_callback_rooms:
            for room in on_join_callback_rooms:
                if self.user_can_go_to_room(user, room):
                    await run_room_function(room, callback, self.internal_data, user)
                    await self.users.set_user_room_by_telegram_id(user.telegram_id, user_migration)
        else:
            for room in self.rooms.get(user_migration):
                if self.user_can_go_to_room(user, room):
                    await self.users.set_user_room_by_telegram_id(user.telegram_id, user_migration)
                    break

        if user.telegram_id in self.internal_data.users_migrations:
            self.internal_data.users_migrations.pop(user.telegram_id)
