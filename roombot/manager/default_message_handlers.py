import aiogram

from roombot.interfaces.IMassageHandler import IMessageHandler
from roombot.types.dataclasses import User
from roombot.types.handler import HandlersTypes
from roombot.interfaces.IUsersTable import IUsersTable
from roombot.types.room import Room
from roombot.utils.runfunc import run_func_as_async, get_kwargs_by_annotations, get_only_the_required_arguments


async def run_room_function(room: Room, message: aiogram.types.Message, internal_data, user: User):
    all_args = {aiogram.types.Message: message, User: user}
    all_args.update(internal_data.global_parameters)
    all_args.update(room.kwargs)
    args = get_kwargs_by_annotations(room.handler.function, all_args)
    args.update(get_only_the_required_arguments(room.handler.function, all_args))
    return await run_func_as_async(room.handler.function, **args)


class MainMessageHandler(IMessageHandler):
    def __init__(self, users: IUsersTable, rooms, internal_data, go_to_room):
        self.users = users
        self.rooms = rooms
        self.internal_data = internal_data
        self.go_to_room = go_to_room

    async def process_message(self, message: aiogram.types.Message):
        user: User
        user_is_at_one_of_rooms: bool = False
        user = await self.users.get_user_by_telegram_id(message.from_user.id)
        for room in self.rooms.get(user.room, get_by_type=HandlersTypes.message):
            if message.content_type in room.handler.content_type:
                user_is_at_one_of_rooms = True
                await run_room_function(room, message, self.internal_data, user)
        if not user_is_at_one_of_rooms:
            await self.go_to_room(message.from_user.id, self.internal_data.start_room)


class CheckUserMessageHandler(IMessageHandler):
    def __init__(self, users: IUsersTable, internal_data):
        self.users = users
        self.internal_data = internal_data

    async def process_message(self, message: aiogram.types.Message):
        if not await self.users.get_user_by_telegram_id(message.from_user.id):
            user_to_add = User(message.from_user.id, message.from_user.first_name, message.from_user.last_name, self.internal_data.default_permissions, self.internal_data.start_room)
            await self.users.add_user(user_to_add)


class UserMigrationMessageRoom(IMessageHandler):
    def __init__(self, users: IUsersTable, rooms, internal_data, user_can_go_to_room):
        self.users = users
        self.rooms = rooms
        self.internal_data = internal_data
        self.user_can_go_to_room = user_can_go_to_room

    async def process_message(self, message: aiogram.types.Message):
        user = await self.users.get_user_by_telegram_id(message.from_user.id)
        user_migration = self.internal_data.users_migrations.get(user.telegram_id)
        if not user_migration: return
        on_join_message_rooms = self.rooms.get(user_migration, get_by_type=HandlersTypes.on_join_message) + self.rooms.get(user_migration, get_by_type=HandlersTypes.on_join_universal)
        if on_join_message_rooms:
            for room in on_join_message_rooms:
                if self.user_can_go_to_room(user, room):
                    await run_room_function(room, message, self.internal_data, user)
                    await self.users.set_user_room_by_telegram_id(user.telegram_id, user_migration)
        else:
            for room in self.rooms.get(user_migration):
                if self.user_can_go_to_room(user, room):
                    await self.users.set_user_room_by_telegram_id(user.telegram_id, user_migration)
                    break

        if user.telegram_id in self.internal_data.users_migrations:
            self.internal_data.users_migrations.pop(user.telegram_id)
