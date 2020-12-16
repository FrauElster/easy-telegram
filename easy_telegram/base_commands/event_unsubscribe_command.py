from telegram import Update, Message
from telegram.ext import CallbackContext

from assests.messages import events_to_unsubscribe_msg, \
    no_events_to_unsubscribe_msg
from easy_telegram.models.User import User


def event_unsubscribe_command(update: Update, context: CallbackContext):
    msg: Message = update.message
    chat_id: str = msg.chat_id
    username: str = msg.from_user.username

    user = User.get_or_create(name=username)

    unsub_events = user.events - user.subscribed_events
    if not unsub_events:
        context.bot.send_message(chat_id, no_events_to_unsubscribe_msg)
        return

    context.bot.send_message(chat_id, events_to_unsubscribe_msg)
    for event in unsub_events:
        context.bot.send_message(chat_id, event.name)
