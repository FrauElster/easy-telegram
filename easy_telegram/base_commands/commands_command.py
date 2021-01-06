from telegram import Update, Message
from telegram.ext import CallbackContext

from easy_telegram.base_commands.messages import NO_COMMANDS_MSG, COMMANDS_MSG
from easy_telegram.models.User import User


def commands_command(update: Update, context: CallbackContext):
    msg: Message = update.message
    chat_id: str = msg.chat_id
    username: str = msg.from_user.username

    user = User.get_or_create(name=username)
    if not user.commands:
        context.bot.send_message(chat_id, NO_COMMANDS_MSG)
        return

    context.bot.send_message(chat_id, COMMANDS_MSG)
    for command in user.commands:
        context.bot.send_message(chat_id, f"/{command.name} - {command.description}")
