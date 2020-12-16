from telegram import Update, Message
from telegram.ext import CallbackContext

from assests.messages import no_events_to_subscribe_msg, events_to_subscribe_msg
from easy_telegram.models.User import User


def event_subscribe_command(update: Update, context: CallbackContext):
    msg: Message = update.message
    chat_id: str = msg.chat_id
    username: str = msg.from_user.username

    user = User.get_or_create(name=username)
    if not user.subscribed_events:
        context.bot.send_message(chat_id, no_events_to_subscribe_msg)
        return

    context.bot.send_message(chat_id, events_to_subscribe_msg)
    for event in user.subscribed_events:
        context.bot.send_message(chat_id, event.name)
