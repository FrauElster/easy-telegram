from telegram import Update, Message
from telegram.ext import CallbackContext

from assests.messages import get_msg, not_banned_yet_msg, unban_notification, unbanned_msg  # type: ignore
from easy_telegram.base_commands.common import get_msg_content
from easy_telegram.models.User import User
from easy_telegram.util.SessionHandler import SessionHandler


def unban_command(update: Update, context: CallbackContext):
    msg: Message = update.message  # type: ignore
    chat_id: int = msg.chat_id

    username: str = get_msg_content(msg.text)[0]  # type: ignore
    session = SessionHandler().session
    user_to_unban = User.get_or_create(session=session, name=username)

    if not user_to_unban.blocked:
        # user is not blocked
        context.bot.send_message(chat_id, get_msg(not_banned_yet_msg, {"user": username}))
        return

    user_to_unban.blocked = False
    session.commit()  # pylint: disable=E1101
    if user_to_unban.chat_id:
        context.bot.send_message(user_to_unban.chat_id, get_msg(unban_notification))
    context.bot.send_message(chat_id, get_msg(unbanned_msg, {"user": username}))
