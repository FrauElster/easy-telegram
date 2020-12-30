from telegram import Update, Message
from telegram.ext import CallbackContext

from assests.messages import get_msg, unknown_event_msg, already_unsubscibed_msg, event_unsubscription_msg  # type: ignore
from easy_telegram.base_commands.common import get_msg_content
from easy_telegram.models.Event import Event
from easy_telegram.models.User import User
from easy_telegram.util.SessionHandler import SessionHandler


def unsubscribe_command(update: Update, context: CallbackContext):
    msg: Message = update.message  # type: ignore
    chat_id: int = msg.chat_id
    username: str = msg.from_user.username  # type: ignore

    event_name: str = get_msg_content(msg.text)[0]  # type: ignore
    if not Event.exists(name=event_name):
        # unknown event
        context.bot.send_message(chat_id, get_msg(unknown_event_msg))
        return

    session = SessionHandler().session
    event: Event = session.query(Event).filter_by(name=event_name).first()  # pylint: disable=E1101
    user = User.get_or_create(session=session, name=username)

    if event not in user.subscribed_events:
        # user has not subscribed
        context.bot.send_message(chat_id, get_msg(already_unsubscibed_msg, {"event": event_name}))
        return

    event.subscribers.remove(user)
    session.commit()  # pylint: disable=E1101

    context.bot.send_message(chat_id, get_msg(event_unsubscription_msg, {"event": event_name}))
