from copy import copy

from typing import Dict

# events
from easy_telegram.util.utils import get_logger

NO_EVENT_SPECIFIED_MSG: str = "No event name specified"
UNKNOWN_EVENT_MSG: str = "Unknown event '<event>'"
EVENT_DISPOSAL_MSG: str = "<event> got removed by server."
EVENT_TRIGGERED_MSG: str = "<event> triggered"
NO_EVENTS_TO_SUBSCRIBE_MSG: str = "No events to subscribe to :("
NO_EVENTS_TO_UNSUBSCRIBE_MSG: str = "No events to unsubscribe from :("
EVENTS_TO_SUBSCRIBE_MSG: str = "Events to subscribe to:"
EVENTS_TO_UNSUBSCRIBE_MSG: str = "Events to unsubscribe from:"
EVENT_SUBSCRIPTION_MSG: str = "You successfully subscribed to <event>"
EVENT_UNSUBSCRIPTION_MSG: str = "You successfully unsubscribed from <event>"
ALREADY_SUBSCRIBED_MSG: str = "You already subscribed <event>"
ALREADY_UNSUBSCRIBED_MSG: str = "You never subscribed <event>"

# commands
NO_COMMANDS_MSG: str = "no commands for you :("
COMMANDS_MSG: str = "You can execute the following commands:"
UNKNOWN_COMMAND_MSG: str = "I do not know the command \"<command>\"..."
COMMAND_SUGGESTION_MSG: str = "Did you mean <command>?"
COMMAND_400: str = "The command does not work like that."

# ban user
BAN_MSG: str = "You are not welcome here! You have been banned!"
BAN_NOTIFICATION: str = "You have been banned! You wont be able to interact with me anymore."
UNBAN_NOTIFICATION: str = "You have been unbanned. You can now talk to me again."
BAN_USER_400_MSG: str = "Usage:\nType the command, the username you want to ban / unban space separated"
ALREADY_BANNED_MSG: str = "<user> is already banned"
NOT_BANNED_YET_MSG: str = "<user> was never banned"
BANNED_MSG: str = "Successfully banned <user>"
UNBANED_MSG: str = "Successfully unbanned <user>"
NO_ADMIN_BAN_MSG: str = "<user> is admin, you cannot ban admins"

# permit user
PERMIT_USER_400_MSG: str = "Usage:\nType the command, the username you want to permit and the permission you want to" \
                           " grant / ungrant all space separated"
UNKNOWN_PERMISSION_MSG: str = "Permission <permission> does not exist"
PERMISSION_NOTIFICATION: str = "You have been permitted '<permission>' :)"
UNPERMISSION_NOTIFICATION: str = "You have been unpermitted '<permission>' :("
USER_ALREADY_PERMITTED_MSG: str = "<user> is already permitted for <permission>"
USER_NOT_PERMITTED_YET_MSG: str = "<user> never was permitted for <permission>"
USER_PERMITTED_MSG: str = "Successfully permitted <user> to <permission>"
USER_UNPERMITTED_MSG: str = "Successfully unpermitted <user> to <permission>"

# general
UNKNOWN_USER_MSG: str = "unknown user \"<user>\""
UNKNOWN_MESSAEG_MSG: str = "I do not know what to do with \"<message>\""
FACT_MSG: str = "Here is something you might have not known:\n\"<fact>\""
GREETING_MSG: str = "Hi, this is my telegram bot. I hope you like it. If you want access and should get one, " \
                    "you know where to find me"

# permission
NOT_PERMITTED_MESSAGE: str = "You are not permitted to do so..."
NO_USERNAME_MSG: str = "You have to have a username to communicate with me"

# statistics
STATISTICS_MSG: str = f"User:\n" \
                      f"- In total <user_total> user have visited this bot\n" \
                      f"- Today <user_today> visited\n\n" \
                      f"Events:\n" \
                      f"- There are <sub_amount> subscriptions on <event_count> events\n" \
                      f"- In average an event has <sub_avg> subscriptions" \
                      f"- <most_subbed> is the most / <least_subbed> the least subscribed event\n\n" \
                      f"Messages:\n" \
                      f"- The bot gets <msg_daily> messages per day\n" \
                      f"- Today it processed <msg_today> so far\n" \
                      f"- <msg_total> were processed in total\n" \
                      f"- The average command respond time is <cmd_response_avg>\n" \
                      f"- Fastest command appears to be <fastest_cmd> / <slowest_cmd> the slowest\n\n" \
                      f"Uptime:\n" \
                      f"- The bot lives since <up_time>\n" \
                      f"- Since its first start in <start_date> it was down for a total of <down_time>."

# default command descriptions
START_COMMAND_DESCRIPTION: str = "Welcomes the user and introduces the bot"
HELP_COMMAND_DESCRIPTION: str = "Shows a list of all available commands with their descriptions"
COMMANDS_COMMAND_DESCRIPTION: str = "Shows a list of all available commands with their descriptions"
EVENTS_COMMAND_DESCRIPTION: str = "Lists all events you can subscribe to"
MY_EVENTS_COMMAND_DESCRIPTION: str = "Lists all events you can unsubscribe from"
SUBSCRIBE_COMMAND_DESCRIPTION: str = "Lets you subscribe to an eventname. Type \"/sub <event_name>\""
SUBSCRIBE_COMMAND_HELP = "Type \"/sub <event_name>\" and replace the <event_name> with the corresponding event. Type \"/events\" to list all available events to sub to"
UNSUBSCRIBE_COMMAND_DESCRIPTION: str = "Lets you unsubscribe from an eventname. Type \"/unsub <event_name>\""
UNSUBSCRIBE_COMMAND_HELP = "Type \"/unsub <event_name>\" and replace the <event_name> with the corresponding event. Type \"/my_events\" to list all available events to unsub from"
PERMIT_COMMAND_DESCRIPTION: str = "Lets you permit a user to a specific permission level. Type \"/permit <username> <permission>\""
PERMIT_COMMAND_HELP = "Type \"/permit <username> <permission>\""
UNPERMIT_COMMAND_DESCRIPTION: str = "Lets you unpermit a user to a specific permission level. Type \"/unpermit <username> <permission>\""
UNPERMIT_COMMAND_HELP = "Type \"/unpermit <username> <permission>\""
BAN_COMMAND_DESCRIPTION: str = "Lets you ban a user so he cant interact with the bot whatsoever"
BAN_COMMAND_HELP = "Type \"/ban <username>\" and replace the username by any name. You cannot ban admins. The banned user will be notified if he ever chatted with the bot"
UNBAN_COMMAND_DESCRIPTION: str = "Lets you unban a user so he can interact with the bot again"
UNBAN_COMMAND_HELP = "Type \"/unban <username>\" and replace the username by any name. The user will be notified if he ever chatted with the bot"

_logger = get_logger("MESSAGES")


def get_msg(message: str, placeholder: Dict[str, str] = None) -> str:
    """
    Returns the specific message with the placeholder in place
    :param message: the base message to replace the placeholders into
    :param placeholder: a dict where k,v are placeholder_to_replace, value_to_replace_with
    :returns a string with the replaced values. If any values were not specified, the placeholder will still be in place
    """
    if placeholder:
        for v in placeholder.values():
            assert isinstance(v, str), f"Placeholder value must be of type str, not {type(v)}"

    _msg: str = copy(message)
    if placeholder:
        for _placeholder, value in placeholder.items():
            if _placeholder not in _msg:
                _logger.warning("Message has no placeholder %s. It gets ignored.", _placeholder)
            _msg = _msg.replace(f"<{_placeholder}>", str(value))

    return _msg
