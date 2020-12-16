from typing import Callable, Optional, List

from telegram import Update
from telegram.ext import CallbackContext

from ..util.LoggerFactory import get_logger
from ..util.State import State


class Command:
    _logger = get_logger("Command")

    name: str
    description: str
    help_usage: str
    args_number: int
    permissions: List[str]
    callback: Callable[[Update, CallbackContext], None]

    def __init__(self, name: str, description: str, callback: Callable[[Update, CallbackContext], None],
                 help_usage: Optional[str] = None, permissions: List[str] = None, args_number: int = 0):
        if permissions is None:
            permissions = set()

        self.name = name
        self.description = description
        self.help_usage = help_usage
        self.args_number = args_number
        self.callback = callback
        self.permissions = permissions

        State().commands.add(self)

    @classmethod
    def exists(cls, **kwargs) -> bool:
        for command in State().commands:
            err = False
            for k, v in kwargs:
                if command[k] != v:
                    err = True
                    break
            if not err:
                return True
        return False

    def __getitem__(self, item):
        if item not in self.__class__.__dict__['__annotations__'].keys():
            raise IndexError(f'{item} is not a attribute of {self.__class__.__name__}')
        return self.__getattribute__(item)
