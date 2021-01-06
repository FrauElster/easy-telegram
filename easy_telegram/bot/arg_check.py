from functools import wraps
from logging import getLogger
from typing import Callable, Optional

from telegram import Update, Message
from telegram.ext import CallbackContext

from easy_telegram.base_commands.common import get_msg_content
from easy_telegram.base_commands.messages import get_msg, COMMAND_400  # type: ignore


class arg_check:
    _logger = getLogger("arg_check")
    _arg_amount: int
    _help_text: Optional[str]

    def __init__(self, arg_amount: int, help_text: Optional[str] = None):
        assert arg_amount >= 0, "You cannot have a negative amount of arguments"
        self._arg_amount = arg_amount
        self._help_text = help_text

    def __call__(self, func: Callable[[Update, CallbackContext], None]) -> Callable[[Update, CallbackContext], None]:
        @wraps(func)
        def wrapper(update: Update, context: CallbackContext):
            msg: Message = update.message  # type: ignore

            if len(get_msg_content(msg.text)) != self._arg_amount:  # type: ignore
                # command needs more / fewer args
                context.bot.send_message(msg.chat_id, get_msg(COMMAND_400))
                if self._help_text:
                    context.bot.send_message(msg.chat_id, self._help_text)
                return
            return func(update, context)

        return wrapper
