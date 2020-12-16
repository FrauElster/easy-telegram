from typing import Optional, List

from telegram import Update, Message
from telegram.ext import CallbackContext

from assests.messages import get_msg, unknown_command_msg, command_suggestion_msg, fact_msg
from easy_telegram.models.Command import Command
from easy_telegram.models.User import User
from easy_telegram.util.SessionHandler import SessionHandler
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

    response: str = get_msg(unknown_command_msg, {"command": f'/{user_command}'})
    if min_distance < 4:
        response += f'\n{get_msg(command_suggestion_msg, {"command": f"/{closest_command.name}"})}'
    else:
        response += f"\n{get_msg(fact_msg, {'fact': random_fact()})}"
    context.bot.send_message(chat_id, response)
