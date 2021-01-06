from telegram import Update, Message
from telegram.ext import CallbackContext

from easy_telegram.base_commands.messages import NO_EVENTS_TO_SUBSCRIBE_MSG, EVENTS_TO_UNSUBSCRIBE_MSG, get_msg
from easy_telegram.models.User import User


def event_subscribe_command(update: Update, context: CallbackContext):
    msg: Message = update.message
    chat_id: str = msg.chat_id
    username: str = msg.from_user.username

    user = User.get_or_create(name=username)
    not_subed = [item for item in user.events if item not in user.subscribed_events]
    if not not_subed:
        context.bot.send_message(chat_id, NO_EVENTS_TO_SUBSCRIBE_MSG)
        return

    event_str = ""
    for event in not_subed:
        event_str += f"\n\t{event.name}"
    context.bot.send_message(chat_id, get_msg(EVENTS_TO_UNSUBSCRIBE_MSG, {"events": event_str}))
