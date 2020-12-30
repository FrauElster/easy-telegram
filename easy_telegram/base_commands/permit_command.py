from telegram import Update, Message
from telegram.ext import CallbackContext

from assests.messages import get_msg, unknown_permission_msg, permission_notification, user_permitted_msg, \
    user_already_permitted_msg
from easy_telegram.base_commands.common import get_msg_content
from easy_telegram.models.Permission import Permission
from easy_telegram.models.User import User
from easy_telegram.util.SessionHandler import SessionHandler


def permit_command(update: Update, context: CallbackContext):
    msg: Message = update.message
    chat_id: int = msg.chat_id

    user_to_perm_name, permission_name = get_msg_content(msg.text)
    if not Permission.exists(name=permission_name):
        # unknown permission
        context.bot.send_message(chat_id, get_msg(unknown_permission_msg, {"permission": permission_name}))
        return

    session = SessionHandler().session
    perm: Permission = session.query(Permission).filter_by(name=permission_name)  # pylint: disable=E1101
    user_to_perm: User = User.get_or_create(session=session, name=user_to_perm_name)
    if user_to_perm.permissions is None:
        user_to_perm.permissions = []

    if perm.name in map(lambda perm_: perm_.name, user_to_perm.permissions):
        # user already permitted
        context.bot.send_message(chat_id, get_msg(user_already_permitted_msg, {"user": user_to_perm_name}))
        return

    user_to_perm.permissions.append(perm)
    session.commit()  # pylint: disable=E1101

    if user_to_perm.chat_id is not None:
        context.bot.send_message(user_to_perm.chat_id,
                                 get_msg(permission_notification, {"permission": permission_name}))
    context.bot.send_message(chat_id, get_msg(user_permitted_msg, {"user": user_to_perm_name}))
