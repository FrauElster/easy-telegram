from telegram import Update, Message
from telegram.ext import CallbackContext

from easy_telegram.base_commands.messages import NO_EVENTS_TO_SUBSCRIBE_MSG, EVENTS_TO_UNSUBSCRIBE_MSG
from easy_telegram.models.User import User


def event_subscribe_command(update: Update, context: CallbackContext):
    msg: Message = update.message
    chat_id: str = msg.chat_id
    username: str = msg.from_user.username

    user = User.get_or_create(name=username)
    if not user.subscribed_events:
        context.bot.send_message(chat_id, NO_EVENTS_TO_SUBSCRIBE_MSG)
        return

    context.bot.send_message(chat_id, EVENTS_TO_UNSUBSCRIBE_MSG)
    for event in user.subscribed_events:
        context.bot.send_message(chat_id, event.name)
