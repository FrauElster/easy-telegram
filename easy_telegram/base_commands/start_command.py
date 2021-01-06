from telegram import Update, Message
from telegram.ext import CallbackContext

from easy_telegram.base_commands.messages import get_msg, GREETING_MSG  # type: ignore


def start_command(update: Update, context: CallbackContext):
    msg: Message = update.message  # type: ignore
    chat_id: int = msg.chat_id

    context.bot.send_message(chat_id, get_msg(GREETING_MSG))
