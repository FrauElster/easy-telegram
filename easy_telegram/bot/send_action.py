from collections import Callable
from functools import wraps

from telegram import Update
from telegram.ext import CallbackContext


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func: Callable):
        @wraps(func)
        def command_func(update: Update, context: CallbackContext, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context, *args, **kwargs)

        return command_func

    return decorator
