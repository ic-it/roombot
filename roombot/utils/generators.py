import aiogram.types

from typing import List
from roombot.manager.manager import RoomsManager
from roombot.exception.utils import KeyboardLevelError
from roombot.exception.utils import KeyboardGeneratorError


class KeyboardButton:
    def __init__(self, text: str = None, room: str = None):
        self.text = text
        self.room = room


def convert_buttons(button_list: list, recursive: int = 0):
    button_list_converted = []
    for item in button_list:
        if isinstance(item, tuple):
            button_list_converted.append(KeyboardButton(*item))
        elif isinstance(item, list):
            if recursive == 1:
                raise KeyboardLevelError("Can be only 1 additional keyboard level")
            button_list_converted.append(convert_buttons(item, recursive + 1))
        elif isinstance(item, KeyboardButton):
            button_list_converted.append(item)
        else:
            raise KeyboardGeneratorError("The keyboard keys can only be of the following types:\n"
                                         "KeyboardButton - One key\n"
                                         "tuple - One key\n"
                                         "list - Many keys on one level\n")
    return button_list_converted


class ReplyKeyboardMarkupGenerator:
    rb: RoomsManager

    def __init__(self, rb: RoomsManager, message_text: str, resize_keyboard: bool = True, one_time_keyboard: bool = False):
        self.rb = rb
        self.keyboard = []
        self.message_text = message_text
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard

    def set_keyboard(self,
                     keyboard: List[
                                    KeyboardButton or
                                    List[KeyboardButton or
                                         tuple] or
                                    tuple
                                    ]
                     ):
        """
        [
            KeyboardButton("any", "any_room"),
            [KeyboardButton("name", "room_name"), KeyboardButton("room", "room_room")]
        ]
        [
            ("Text", "room"),
            [("Text2", "room2"), ("Text3", "room3")]
        ]
        """
        self.keyboard = convert_buttons(keyboard)

    def process(self, message_text: str):
        message_keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=self.resize_keyboard,
                                                             one_time_keyboard=self.one_time_keyboard)
        for item in message_keyboard:
            if isinstance(item, KeyboardButton):
                key = aiogram.types.KeyboardButton(item.text)
                message_keyboard.add(key)
            elif isinstance(item, list):
                key = aiogram.types.KeyboardButton(*[i.text for i in item])
                message_keyboard.add(key)


