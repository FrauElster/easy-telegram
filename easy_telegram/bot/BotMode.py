from enum import Enum


class BotMode(Enum):
    WHITELIST = "whitelist"
    BLACKLIST = "blacklist"


def get_mode():
    from easy_telegram.util.utils import get_env

    if len(get_env("TELEGRAM_WHITELIST", type_=str, default="")) > 0:
        return BotMode.WHITELIST
    return BotMode.BLACKLIST
