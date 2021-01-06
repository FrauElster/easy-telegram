from enum import Enum


class BotMode(Enum):
    WHITELIST = "whitelist"
    BLACKLIST = "blacklist"


MODE = BotMode.WHITELIST
