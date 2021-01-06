from functools import wraps
from logging import getLogger
from typing import Callable

from telegram import Update, Message
from telegram.ext import CallbackContext

from easy_telegram.base_commands.messages import get_msg, NO_USERNAME_MSG
from easy_telegram.models.User import User
from easy_telegram.util.SessionHandler import SessionHandler


def username_check(func: Callable[[Update, CallbackContext], None]):
    @wraps(func)
    def wrapper(update: Update, context: CallbackContext):
        msg: Message = update.message

        try:
            if not msg.from_user.username:
                context.bot.send_message(msg.chat_id, get_msg(NO_USERNAME_MSG))
                return
        except KeyError as e:
            getLogger("username_check").warning(e)
            return

        session = SessionHandler().session
        user = User.get_or_create(session=session, name=msg.from_user["username"])
        user.chat_id = msg.chat_id
        session.commit()  # pylint: disable=E1101

        return func(update, context)

    return wrapper
