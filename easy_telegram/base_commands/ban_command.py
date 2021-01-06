from telegram import Update, Message
from telegram.ext import CallbackContext

from easy_telegram.base_commands.messages import get_msg, ALREADY_BANNED_MSG, NO_ADMIN_BAN_MSG, BAN_NOTIFICATION, BANNED_MSG
from easy_telegram.base_commands.common import get_msg_content
from easy_telegram.models.User import User
from easy_telegram.util.SessionHandler import SessionHandler


def ban_command(update: Update, context: CallbackContext):
    msg: Message = update.message
    chat_id: int = msg.chat_id

    username: str = get_msg_content(msg.text)[0]
    session = SessionHandler().session
    user_to_ban = User.get_or_create(session=session, name=username)

    if user_to_ban.is_admin:
        # user is admin
        context.bot.send_message(chat_id, get_msg(NO_ADMIN_BAN_MSG, {"user": username}))
        return

    if user_to_ban.blocked:
        # user already blocked
        context.bot.send_message(chat_id, get_msg(ALREADY_BANNED_MSG, {"user": username}))
        return

    user_to_ban.blocked = True
    session.commit()  # pylint: disable=E1101
    if user_to_ban.chat_id:
        context.bot.send_message(user_to_ban.chat_id, get_msg(BAN_NOTIFICATION))
    context.bot.send_message(chat_id, get_msg(BANNED_MSG, {"user": username}))
