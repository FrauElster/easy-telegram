from typing import Callable
from functools import wraps

from telegram import Update
from telegram.ext import CallbackContext


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func: Callable[[Update, CallbackContext], None]):
        @wraps(func)
        def command_func(update: Update, context: CallbackContext):
            context.bot.send_chat_action(chat_id=update.message.chat_id, action=action)  # type: ignore
            return func(update, context)

        return command_func

    return decorator
