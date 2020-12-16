from telegram import Message, Update
from telegram.ext import CallbackContext

from assests.messages import get_msg, unknown_message_msg, fact_msg
from easy_telegram.base_commands.unknown_command import unknown_command
from easy_telegram.util.random_fact import random_fact


def unknown_message(update: Update, context: CallbackContext):
    msg: Message = update.message
    chat_id: int = msg.chat_id

    if msg.text[0] == "/":
        unknown_command(update, context)
        return

    response: str = get_msg(unknown_message_msg, {"message": msg.text})
    response += f"\n{get_msg(fact_msg, {'fact': random_fact()})}"
    context.bot.send_message(chat_id, response)
