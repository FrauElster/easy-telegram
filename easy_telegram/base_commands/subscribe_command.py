from telegram import Update, Message
from telegram.ext import CallbackContext

from easy_telegram.base_commands.messages import get_msg, UNKNOWN_EVENT_MSG, ALREADY_SUBSCRIBED_MSG, NOT_PERMITTED_MESSAGE, \
    EVENT_SUBSCRIPTION_MSG
from easy_telegram.base_commands.common import get_msg_content
from easy_telegram.models.Event import Event
from easy_telegram.models.User import User
from easy_telegram.util.SessionHandler import SessionHandler


def subscribe_command(update: Update, context: CallbackContext):
    msg: Message = update.message  # type: ignore
    chat_id: int = msg.chat_id
    username: str = msg.from_user.username  # type: ignore

    event_name: str = get_msg_content(msg.text)[0]  # type: ignore
    if not Event.exists(name=event_name):
        # unknown event
        context.bot.send_message(chat_id, get_msg(UNKNOWN_EVENT_MSG))
        return

    session = SessionHandler().session
    event: Event = session.query(Event).filter_by(name=event_name).first()  # pylint: disable=E1101
    user = User.get_or_create(session=session, name=username)

    if event in user.subscribed_events:
        # user has already subscribed
        context.bot.send_message(chat_id, get_msg(ALREADY_SUBSCRIBED_MSG, {"event": event_name}))
        return

    if not user.is_permitted(event):
        # user is not permitted
        context.bot.send_message(chat_id, get_msg(NOT_PERMITTED_MESSAGE))
        return

    if event.subscribers is None:
        event.subscribers = []
    event.subscribers.append(user)
    session.commit()  # pylint: disable=E1101

    context.bot.send_message(chat_id, get_msg(EVENT_SUBSCRIPTION_MSG, {"event": event_name}))
