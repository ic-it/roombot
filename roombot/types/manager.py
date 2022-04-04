import aiogram

from dataclasses import dataclass

from roombot.interfaces.IMassageHandler import IMessageHandler
from roombot.interfaces.ICallbackHandler import ICallbackHandler
from roombot.interfaces.IErrorHandler import IErrorHandler
from roombot.types.room import RoomsStack
from roombot.interfaces.IUsersTable import IUsersTable
from roombot.rooms_container.rooms_container import RoomsContainer
from roombot.types.handler import MessageHandlersStack, CallbackHandlersStack, ErrorHandlerStack, PreCheckoutQueryHandlerStack
from roombot.manager.actions_with_user import ActionsWithUser


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
    error: ErrorHandlerStack
    pre_checkout_query: PreCheckoutQueryHandlerStack


class IRoomsManager:
    rooms: RoomsStack
    users: IUsersTable
    internal_data: ManagerInternalData
    handlers: HandlersHab
    default_handlers_included: bool
    actions_with_user: ActionsWithUser

    def __init__(self,
                 users: IUsersTable,
                 start_room: str,
                 default_permissions: str = "",
                 include_default_handlers: bool = False
                 ): ...

    def include_default_handlers(self): ...
    def append_rooms(self, rooms_container: RoomsContainer): ...
    def add_message_handler(self, handler: IMessageHandler, position_in_stack: int = None): ...
    def add_error_handler(self, handler: IErrorHandler, position_in_stack: int = None): ...
    def add_callback_handler(self, handler: ICallbackHandler, position_in_stack: int = None): ...
    def add_global_parameters(self, **kwargs): ...
    def get_global_parameter(self, key: str): ...
    async def process_message(self, message: aiogram.types.Message): ...
    async def process_callback(self, callback: aiogram.types.CallbackQuery): ...
    async def process_error(self, exception: Exception, text: str): ...