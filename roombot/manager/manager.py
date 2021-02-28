import aiogram

from typing import List, Any
from dataclasses import dataclass
from .actions_with_user import ActionsWithUser
from roombot.types.room import RoomsStack
from roombot.types.dataclasses import User
from roombot.types.handler import MessageHandlersStack, CallbackHandlersStack
from roombot.interfaces.IUsersTable import IUsersTable
from roombot.rooms_container.rooms_container import RoomsContainer
from roombot.utils.runfunc import run_func_as_async, get_kwargs_by_annotations, get_only_the_required_arguments
from .default_message_handlers import MainMessageHandler, UserMigrationMessageRoom, CheckUserMessageHandler
from .default_callback_handlers import MainCallbackHandler, UserMigrationCallbackRoom, CheckUserCallbackHandler


@dataclass
class ManagerInternalData:
    """
    А это просто зборище всех очень нужных переменных, котрые в основном классе выглядели бы не крассиво и легче передвать именно
        dataclass, а не по одной переменной :)
    """
    start_room: str
    default_permissions: str
    users_migrations: dict
    global_parameters: dict


@dataclass
class HandlersHab:
    """
    Это короче то где будут хранится все ссылки на перехватчики событий.
    """
    message: MessageHandlersStack
    callback: CallbackHandlersStack


class RoomsManager:
    """
    Главный класс.
    Тут вроде все работает по человечески.
    """
    rooms: RoomsStack
    users: IUsersTable
    internal_data: ManagerInternalData
    handlers: HandlersHab
    default_handlers_included: bool

    def __init__(self,
                 users: IUsersTable,
                 start_room: str,
                 default_permissions: str = "",
                 include_default_handlers: bool = False
                 ):
        self.users = users
        self.rooms = RoomsStack()
        self.internal_data = ManagerInternalData(start_room, default_permissions, {}, {})
        self.handlers = HandlersHab(MessageHandlersStack(), CallbackHandlersStack())
        self.actions_with_user = ActionsWithUser(self.users, self.internal_data, self.rooms)
        self.default_handlers_included = False
        if include_default_handlers:
            self.include_default_handlers()

    def include_default_handlers(self):
        if self.default_handlers_included:
            return
        check_user_handler_message = CheckUserMessageHandler(self.users, self.internal_data)
        main_handler_message = MainMessageHandler(self.users, self.rooms, self.internal_data, self.actions_with_user.go_to_room)
        user_migration_handler_message = UserMigrationMessageRoom(self.users, self.rooms, self.internal_data,
                                                          self.actions_with_user.user_can_go_to_room)

        check_user_handler_callback = CheckUserCallbackHandler(self.users, self.internal_data)
        main_handler_callback = MainCallbackHandler(self.users, self.rooms, self.internal_data, self.actions_with_user.go_to_room)
        user_migration_handler_callback = UserMigrationCallbackRoom(self.users, self.rooms, self.internal_data,
                                                          self.actions_with_user.user_can_go_to_room)

        self.handlers.message.add(check_user_handler_message)
        self.handlers.message.add(main_handler_message)
        self.handlers.message.add(user_migration_handler_message)

        self.handlers.callback.add(check_user_handler_callback)
        self.handlers.callback.add(main_handler_callback)
        self.handlers.callback.add(user_migration_handler_callback)

        self.default_handlers_included = True

    def append_rooms(self, rooms_container: RoomsContainer):
        self.rooms.add(rooms_container.rooms)

    def add_message_handler(self, handler: Any):
        self.handlers.message.add(handler)

    def add_global_parameters(self, **kwargs):
        self.internal_data.global_parameters.update(kwargs)

    async def process_message(self, message: aiogram.types.Message):
        for handler in self.handlers.message.get_all():
            kwargs = get_kwargs_by_annotations(handler, {aiogram.types.Message: message
                                                         })
            await run_func_as_async(handler, **kwargs)

    async def process_callback(self, callback: aiogram.types.CallbackQuery):
        for handler in self.handlers.callback.get_all():
            all_args = {
                aiogram.types.CallbackQuery: callback
             }
            kwargs = get_kwargs_by_annotations(handler, all_args)
            await run_func_as_async(handler, **kwargs)

