from typing import Optional

from telegram import Update, Message
from telegram.ext import CallbackContext

from easy_telegram.base_commands.messages import get_msg, UNKNOWN_COMMAND_MSG, COMMAND_SUGGESTION_MSG, FACT_MSG
from easy_telegram.models.Command import Command
from easy_telegram.models.User import User
from easy_telegram.util.random_fact import random_fact
from easy_telegram.util.utils import levenshtein


def unknown_command(update: Update, context: CallbackContext):
    msg: Message = update.message
    chat_id: int = msg.chat_id
    username: str = msg.from_user.username
    user_command: str = msg.text.split(" ")[0][1:]

    user = User.get_or_create(name=username)

    min_distance: int = 1000
    closest_command: Optional[Command] = None

    for command in user.commands:
        if levenshtein(command.name, user_command) < min_distance:
            min_distance = levenshtein(command.name, user_command)
            closest_command = command

    response: str = get_msg(UNKNOWN_COMMAND_MSG, {"command": f'/{user_command}'})
    if min_distance < 4:
        response += f'\n{get_msg(COMMAND_SUGGESTION_MSG, {"command": f"/{closest_command.name}"})}'
    else:
        response += f"\n{get_msg(FACT_MSG, {'fact': random_fact()})}"
    context.bot.send_message(chat_id, response)
