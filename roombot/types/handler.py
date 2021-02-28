from typing import Any, List
from roombot.interfaces.IMassageHandler import IMessageHandler
from roombot.interfaces.ICallbackHandler import ICallbackHandler


class Handler:
    function: Any
    handler_type: int
    content_type: List[str]

    def __init__(self, h_type: int, content_type: List[str], func: Any):
        self.content_type = content_type
        self.handler_type = h_type
        self.function = func


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


class MessageHandlersStack:
    """
    Это все комнаты для обработки сообщений.
    """
    message_handlers: List[IMessageHandler]

    def __init__(self, *handlers):
        self.message_handlers = []
        self.message_handlers += handlers

    def add(self, handler: IMessageHandler):
        self.message_handlers.append(handler)
        return self

    def get_all(self):
        loaded_handlers = []
        for i in self.message_handlers:
            if not isinstance(i, IMessageHandler):
                continue
            loaded_handlers.append(i.process_message)
        return loaded_handlers


class CallbackHandlersStack:
    """
    Это все комнаты для обработки callback.
    """
    callback_handlers: List[ICallbackHandler]

    def __init__(self, *handlers):
        self.callback_handlers = []
        self.callback_handlers += handlers

    def add(self, handler: ICallbackHandler):
        self.callback_handlers.append(handler)
        return self

    def get_all(self):
        loaded_handlers = []
        for i in self.callback_handlers:
            if not isinstance(i, ICallbackHandler):
                continue
            loaded_handlers.append(i.process_callback)
        return loaded_handlers

