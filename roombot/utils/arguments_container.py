from dataclasses import dataclass
from tgusers.dataclasses.args_container import ArgumentsBox
from typing import List
from tgusers.dataclasses.rooms import Argument


class ArgumentsContainer:
    def __init__(self):
        self.arguments_list: List[ArgumentsBox]
        self.arguments_list = []


    def add_arguments_to_room(self, room_name: str, arguments: dict):
        """
        :param room_name:
        :param arguments:
            Dict of {
                        annotation: value,
                        annotation1: value1,
                        annotation2: value2,
                    }
        :return:
        """
        if not isinstance(arguments, dict):
            raise Exception("Arguments must be an <dict>")
        arguments_list = []
        for argument in arguments:
            one_argument = Argument(value=arguments.get(argument), annotation=argument)
            arguments_list.append(one_argument)
        argument_pack = ArgumentsBox(room_name, arguments_list)
        self.arguments_list.append(argument_pack)
