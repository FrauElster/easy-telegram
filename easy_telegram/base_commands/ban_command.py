from telegram import Update, Message
from telegram.ext import CallbackContext

from assests.messages import get_msg, already_banned_msg, no_admin_ban_msg, ban_notification, banned_msg
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
        context.bot.send_message(chat_id, get_msg(no_admin_ban_msg, {"user": username}))
        return

    if user_to_ban.blocked:
        # user already blocked
        context.bot.send_message(chat_id, get_msg(already_banned_msg, {"user": username}))
        return

    user_to_ban.blocked = True
    session.commit()
    if user_to_ban.chat_id:
        context.bot.send_message(user_to_ban.chat_id, get_msg(ban_notification))
    context.bot.send_message(chat_id, get_msg(banned_msg, {"user": username}))
