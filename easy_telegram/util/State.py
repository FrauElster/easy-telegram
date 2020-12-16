from .singleton import singleton


class State:
    __metaclass__ = singleton

    commands = set()
