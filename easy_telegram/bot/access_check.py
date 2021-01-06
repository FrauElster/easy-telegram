from functools import wraps
from typing import Callable, Set, List

from telegram import Update, Message
from telegram.ext import CallbackContext

from easy_telegram.base_commands.messages import BAN_MSG, NOT_PERMITTED_MESSAGE
from easy_telegram.bot.BotMode import get_mode, BotMode
from easy_telegram.models.User import User
from easy_telegram.util.utils import get_logger


class access_check:
    _logger = get_logger("access_check")
    _permissions: Set[str]

    def __init__(self, permissions: List[str]):
        self._permissions = permissions

    def __call__(self, func: Callable[[Update, CallbackContext], None]) -> Callable[[Update, CallbackContext], None]:
        @wraps(func)
        def wrapper(update: Update, context: CallbackContext):
            msg: Message = update.message
            username: str = msg.from_user.username

            user = User.get_or_create(name=username)

            if user.is_admin:
                # user is admin
                return func(update, context)

            if user.blocked:
                # user is blocked
                self._logger.info("Blocked user %s tried to send msg: '%s'", user.name, msg.text)
                context.bot.send_message(chat_id=msg.chat_id, text=BAN_MSG)
                return

            if get_mode() == BotMode.WHITELIST and not user.whitelisted:
                # user is not whitelisted
                self._logger.info("Non whitelisted user %s tried to send msg: '%s'", user.name, msg.text)
                context.bot.send_message(chat_id=msg.chat_id,
                                         text=NOT_PERMITTED_MESSAGE)
                return

            if not self._permissions:
                return func(update, context)
            user_perms: Set[str] = set()
            if user.permissions is not None:
                user_perms = set(map(lambda perm_: perm_.name, user.permissions))
            for user_perm in user_perms:
                if user_perm in self._permissions:
                    return func(update, context)
            # user is not permitted
            self._logger.info("user %s has none of the required permissions ('%s') to send msg: '%s'", user.name,
                              ", ".join(self._permissions), msg.text)
            context.bot.send_message(chat_id=msg.chat_id,
                                     text=NOT_PERMITTED_MESSAGE)
            return

        return wrapper
