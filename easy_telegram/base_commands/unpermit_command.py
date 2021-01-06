from telegram import Update, Message
from telegram.ext import CallbackContext

from easy_telegram.base_commands.messages import get_msg, UNKNOWN_PERMISSION_MSG, USER_NOT_PERMITTED_YET_MSG, UNPERMISSION_NOTIFICATION, \
    USER_UNPERMITTED_MSG
from easy_telegram.base_commands.common import get_msg_content
from easy_telegram.models.Permission import Permission
from easy_telegram.models.User import User
from easy_telegram.util.SessionHandler import SessionHandler


def unpermit_command(update: Update, context: CallbackContext):
    msg: Message = update.message  # type: ignore
    chat_id: int = msg.chat_id

    user_to_perm_name, permission_name = get_msg_content(msg.text)  # type: ignore
    if not Permission.exists(name=permission_name):
        # unknown permission
        context.bot.send_message(chat_id, get_msg(UNKNOWN_PERMISSION_MSG, {"permission": permission_name}))
        return

    session = SessionHandler().session
    perm: Permission = session.query(Permission).filter_by(name=permission_name)  # pylint: disable=E1101
    user_to_unperm: User = User.get_or_create(session=session, name=user_to_perm_name)
    if user_to_unperm.permissions is None:
        user_to_unperm.permissions = []

    if perm.name not in map(lambda perm_: perm_.name, user_to_unperm.permissions):
        # user does not have permission
        context.bot.send_message(chat_id, get_msg(USER_NOT_PERMITTED_YET_MSG, {"user": user_to_perm_name}))
        return

    user_to_unperm.permissions.remove(perm)
    session.commit()  # pylint: disable=E1101

    if user_to_unperm.chat_id is not None:
        context.bot.send_message(user_to_unperm.chat_id,
                                 get_msg(UNPERMISSION_NOTIFICATION, {"permission": permission_name}))
    context.bot.send_message(chat_id, get_msg(USER_UNPERMITTED_MSG, {"user": user_to_perm_name}))
