from telegram import Update, Message
from telegram.ext import CallbackContext

from assests.messages import no_commands_msg, commands_msg
from easy_telegram.models.User import User


def commands_command(update: Update, context: CallbackContext):
    msg: Message = update.message
    chat_id: str = msg.chat_id
    username: str = msg.from_user.username

    user = User.get_or_create(name=username)
    if not user.commands:
        context.bot.send_message(chat_id, no_commands_msg)
        return

    context.bot.send_message(chat_id, commands_msg)
    for command in user.commands:
        context.bot.send_message(chat_id, f"/{command.name} - {command.description}")
