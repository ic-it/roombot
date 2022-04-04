from typing import Any, List
from roombot.interfaces.IMassageHandler import IMessageHandler
from roombot.interfaces.ICallbackHandler import ICallbackHandler
from roombot.interfaces.IErrorHandler import IErrorHandler
from roombot.interfaces.IHandler import IHandler


class Handler:
    function: Any
    handler_type: int
    content_type: List[str]
    room_filter: Any

    def __init__(self, h_type: int, content_type: List[str], func: Any, room_filter: (Any or None)):
        self.content_type = content_type
        self.handler_type = h_type
        self.function = func
        self.room_filter = room_filter


class HandlersTypes:
    callback: int = 1
    message: int = 2
    on_join_message: int = 3
    on_join_callback: int = 4
    on_join_universal: int = 5
    compatibility = [
        [callback, on_join_callback, on_join_universal],
        [message, on_join_message, on_join_universal]
    ]

    @staticmethod
    def in_types(type_num: int):
        if type_num in (HandlersTypes.callback,
                        HandlersTypes.message,
                        HandlersTypes.on_join_message,
                        HandlersTypes.on_join_callback,
                        HandlersTypes.on_join_universal
                        ):
            return True
        return False

    @staticmethod
    def are_compatibility(*h_types):
        for i in HandlersTypes.compatibility:
            are_compat = True
            for h_type in h_types:
                if h_type not in i:
                    are_compat = False
            if are_compat:
                return True
        return False


class HandlersStack:
    handlers_interface: IHandler = IHandler
    handlers: List[handlers_interface]

    def __init__(self):
        self.handlers = []

    def add(self, handler: handlers_interface, position_in_stack: int = None):
        if not isinstance(handler, self.handlers_interface):
            raise Exception("Incorrect handler type")
        else:
            if position_in_stack is not None:
                self.handlers.insert(position_in_stack, handler)
            else:
                self.handlers.append(handler)
            return self

    def get_all(self):
        return [i.process for i in self.handlers]


class MessageHandlersStack(HandlersStack):
    handlers_interface: IMessageHandler = IMessageHandler


class CallbackHandlersStack(HandlersStack):
    handlers_interface: ICallbackHandler = ICallbackHandler


class ErrorHandlerStack(HandlersStack):
    handlers_interface: IErrorHandler = IErrorHandler


class PreCheckoutQueryHandlerStack(HandlersStack):
    handlers_interface: IHandler = IHandler

