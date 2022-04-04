import aiogram

from typing import List, Any
from dataclasses import dataclass
from .actions_with_user import ActionsWithUser
from ..types.room import RoomsStack
from ..types.datatypes import User
from ..types.manager import IRoomsManager, ManagerInternalData, HandlersHab
from ..types.handler import MessageHandlersStack, CallbackHandlersStack, ErrorHandlerStack, PreCheckoutQueryHandlerStack
from ..interfaces.IUsersTable import IUsersTable
from ..interfaces.IMassageHandler import IMessageHandler
from ..interfaces.ICallbackHandler import ICallbackHandler
from ..interfaces.IErrorHandler import IErrorHandler, IHandler
from ..rooms_container.rooms_container import RoomsContainer
from ..utils.runfunc import run_func_as_async, get_kwargs_by_annotations, get_only_the_required_arguments
from .default_message_handlers import MainMessageHandler, UserMigrationMessageRoom, CheckUserMessageHandler
from .default_callback_handlers import MainCallbackHandler, UserMigrationCallbackRoom, CheckUserCallbackHandler


class RoomsManager(IRoomsManager):
    """
    Главный класс.
    Тут вроде все работает по человечески.
    """
    rooms: RoomsStack
    users: IUsersTable
    internal_data: ManagerInternalData
    handlers: HandlersHab
    default_handlers_included: bool
    actions_with_user: ActionsWithUser

    def __init__(self, users: IUsersTable, start_room: str, default_permissions: str = "",
                 include_default_handlers: bool = False):
        super().__init__(users, start_room, default_permissions, include_default_handlers)
        self.users = users
        self.rooms = RoomsStack()
        self.internal_data = ManagerInternalData(start_room, default_permissions, {}, {})
        self.handlers = HandlersHab(MessageHandlersStack(), CallbackHandlersStack(), ErrorHandlerStack(), PreCheckoutQueryHandlerStack())
        self.actions_with_user = ActionsWithUser(self.users, self.internal_data, self.rooms)
        self.default_handlers_included = False
        if include_default_handlers:
            self.include_default_handlers()

    def include_default_handlers(self):
        if self.default_handlers_included:
            return
        check_user_handler_message = CheckUserMessageHandler(self.users, self.internal_data)
        main_handler_message = MainMessageHandler(self.users, self.rooms, self.internal_data,
                                                  self.actions_with_user.go_to_room)
        user_migration_handler_message = UserMigrationMessageRoom(self.users, self.rooms, self.internal_data,
                                                                  self.actions_with_user.user_can_go_to_room)

        check_user_handler_callback = CheckUserCallbackHandler(self.users, self.internal_data)
        main_handler_callback = MainCallbackHandler(self.users, self.rooms, self.internal_data,
                                                    self.actions_with_user.go_to_room)
        user_migration_handler_callback = UserMigrationCallbackRoom(self.users, self.rooms, self.internal_data,
                                                                    self.actions_with_user.user_can_go_to_room)

        self.handlers.message.add(check_user_handler_message)
        self.handlers.message.add(main_handler_message)
        self.handlers.message.add(user_migration_handler_message)

        self.handlers.callback.add(check_user_handler_callback)
        self.handlers.callback.add(main_handler_callback)
        self.handlers.callback.add(user_migration_handler_callback)

        self.default_handlers_included = True

    # def __getitem__(self, item):
    #     action, data = item
    #     if action == "set_user_class":
    #         self.users = data
    #     return self

    def append_rooms(self, rooms_container: RoomsContainer):
        self.rooms.add(rooms_container.rooms)

    def add_message_handler(self, handler: IMessageHandler, position_in_stack: int = None):
        self.handlers.message.add(handler, position_in_stack)

    def add_error_handler(self, handler: IErrorHandler, position_in_stack: int = None):
        self.handlers.error.add(handler, position_in_stack)

    def add_callback_handler(self, handler: ICallbackHandler, position_in_stack: int = None):
        self.handlers.callback.add(handler, position_in_stack)

    def add_pre_checkout_query_handler(self, handler: IHandler, position_in_stack: int = None):
        self.handlers.pre_checkout_query.add(handler, position_in_stack)

    def add_global_parameters(self, **kwargs):
        self.internal_data.global_parameters.update(kwargs)

    def get_global_parameter(self, key: str):
        return self.internal_data.global_parameters.get(key)

    async def process_message(self, message: aiogram.types.Message):
        for handler in self.handlers.message.get_all():
            all_args = {
                aiogram.types.Message: message
            }
            kwargs = get_kwargs_by_annotations(handler, all_args)
            kwargs["rooms_manager"] = self
            await run_func_as_async(handler, **kwargs)

    async def process_callback(self, callback: aiogram.types.CallbackQuery):
        for handler in self.handlers.callback.get_all():
            all_args = {
                aiogram.types.CallbackQuery: callback,
                IRoomsManager: self,
                RoomsManager: self
            }
            kwargs = get_kwargs_by_annotations(handler, all_args)
            kwargs["rooms_manager"] = self
            await run_func_as_async(handler, **kwargs)

    async def process_error(self, exception: Exception, text: str):
        for handler in self.handlers.error.get_all():
            all_args = {
                Exception: exception,
                str: text,
                IRoomsManager: self,
                RoomsManager: self
            }
            kwargs = get_kwargs_by_annotations(handler, all_args)
            kwargs["rooms_manager"] = self
            kwargs["text"] = text
            await run_func_as_async(handler, **kwargs)

    async def process_pre_checkout_query(self, pre_checkout_query_handler: aiogram.types.PreCheckoutQuery):
        for handler in self.handlers.pre_checkout_query.get_all():
            all_args = {
                aiogram.types.PreCheckoutQuery: pre_checkout_query_handler,
                IRoomsManager: self,
                RoomsManager: self
            }
            kwargs = get_kwargs_by_annotations(handler, all_args)
            kwargs["rooms_manager"] = self
            await run_func_as_async(handler, **kwargs)

