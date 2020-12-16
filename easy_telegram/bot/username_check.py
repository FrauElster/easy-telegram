from functools import wraps
from typing import Callable

from telegram import Update, Message
from telegram.ext import CallbackContext

from assests.messages import get_msg, no_username_msg
from easy_telegram.models.User import User
from easy_telegram.util.LoggerFactory import get_logger
from easy_telegram.util.SessionHandler import SessionHandler


def username_check(func: Callable[[Update, CallbackContext], None]):
    @wraps(func)
    def wrapper(update: Update, context: CallbackContext):
        msg: Message = update.message

        try:
            if not msg.from_user.username:
                context.bot.send_message(msg.chat_id, get_msg(no_username_msg))
                return
        except Exception as e:
            get_logger("username_check").warning(e)
            return

        session = SessionHandler().session
        user = User.get_or_create(session=session, name=msg.from_user["username"])
        user.chat_id = msg.chat_id
        session.commit()

        return func(update, context)

    return wrapper
