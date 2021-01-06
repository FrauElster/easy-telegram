from telegram import Update, Message
from telegram.ext import CallbackContext

from easy_telegram.base_commands.messages import EVENTS_TO_UNSUBSCRIBE_MSG, \
    NO_EVENTS_TO_UNSUBSCRIBE_MSG, get_msg
from easy_telegram.models.User import User


def event_unsubscribe_command(update: Update, context: CallbackContext):
    msg: Message = update.message
    chat_id: str = msg.chat_id
    username: str = msg.from_user.username

    user = User.get_or_create(name=username)

    if not user.subscribed_events:
        context.bot.send_message(chat_id, NO_EVENTS_TO_UNSUBSCRIBE_MSG)
        return

    event_str = ""
    for event in user.subscribed_events:
        event_str += f"\n\t{event.name}"
    context.bot.send_message(chat_id, get_msg(EVENTS_TO_UNSUBSCRIBE_MSG, {"events": event_str}))
