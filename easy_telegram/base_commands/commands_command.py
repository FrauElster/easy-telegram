from telegram import Update, Message
from telegram.ext import CallbackContext

from easy_telegram.base_commands.messages import NO_COMMANDS_MSG, COMMANDS_MSG, get_msg
from easy_telegram.models.User import User


def commands_command(update: Update, context: CallbackContext):
    msg: Message = update.message
    chat_id: str = msg.chat_id
    username: str = msg.from_user.username

    user = User.get_or_create(name=username)
    if not user.commands:
        context.bot.send_message(chat_id, NO_COMMANDS_MSG)
        return

    commands: str = ""
    for command in user.commands:
        commands += f"\n\t/{command.name} - {command.description}"

    context.bot.send_message(chat_id, get_msg(COMMANDS_MSG, {"commands": commands}))
