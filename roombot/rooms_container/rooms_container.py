from typing import List
from roombot.types.room import Room
from roombot.types.handler import Handler
from roombot.types.handler import HandlersTypes
from roombot.exception.room_container import IncorrectHandlerType


class RoomsContainer:
    rooms: List[Room]

    def __init__(self):
        self.rooms = []

    def add_room(self, name: str, room_type: int, content_type=None, permissions=None, **kwargs):
        if content_type is None:
            content_type = []
        if permissions is None:
            permissions = []

        def decorator(parameters):
            if isinstance(parameters, dict):
                past_room_type = parameters.get("past_room_type")
                func = parameters.get("func")
            else:
                past_room_type = None
                func = parameters
            if past_room_type is not None:
                if not HandlersTypes.are_compatibility(past_room_type, room_type):
                    raise Exception("Un compatibility rooms. ")
            if not HandlersTypes.in_types(room_type):
                raise IncorrectHandlerType("Incorrect handler type")
            room_handler = Handler(room_type, content_type, func)
            room = Room(name, room_handler, kwargs, permissions)
            self.rooms.append(room)
            return {"func": func, "past_room_type": room.handler.handler_type}
        return decorator

