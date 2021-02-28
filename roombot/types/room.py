from roombot.types.handler import Handler
from typing import Any, List


class Room:
    name: str
    kwargs: dict
    handler: Handler
    permissions: List[str or None]

    def __init__(self, room_name: str, room_handler: Handler, kwargs: dict, permissions: List[str or None]):
        self.name    = room_name
        self.kwargs  = kwargs
        self.handler = room_handler
        self.permissions = permissions


class RoomsStack:
    """
    Тут банально хранятся все данные о комнатах. Соритровка такая:
        1. Есть имя, оно как ключ в dict
        2. Этому имени соотвецтвует dict. В котором ключ это тип, а value - это комнаты.
    """
    rooms: dict[str, dict[int, List[Room]]]

    def __init__(self):
        self.rooms = {}

    def add(self, rooms: (Room or List[Room])):
        if isinstance(rooms, Room):
            rooms = [rooms]
        for room in rooms:
            if room.name not in self.rooms:
                self.rooms[room.name] = {}
            if not self.rooms[room.name].get(room.handler.handler_type):
                self.rooms[room.name][room.handler.handler_type] = []
            self.rooms[room.name][room.handler.handler_type].append(room)

    def get(self, room_name: str, get_by_type: int = None) -> List[Room]:
        rooms_by_name = self.rooms.get(room_name)
        if rooms_by_name is None:
            return []
        if get_by_type is not None:
            return rooms_by_name.get(get_by_type) or []
        return_list = []
        for i in rooms_by_name:
            return_list += rooms_by_name.get(i)
        return return_list
