from telegram import Update, Message
from telegram.ext import CallbackContext

from assests.messages import get_msg, greeting_msg  # type: ignore


def start_command(update: Update, context: CallbackContext):
    msg: Message = update.message  # type: ignore
    chat_id: int = msg.chat_id

    context.bot.send_message(chat_id, get_msg(greeting_msg))
