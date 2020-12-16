from copy import copy

from typing import Dict

# events
no_event_specified_msg: str = "No event name specified"
unknown_event_msg: str = "Unknown event '<event>'"
event_disposal_msg: str = "<event> got removed by server."
event_triggered_msg: str = "<event> triggered"
no_events_to_subscribe_msg: str = "No events to subscribe to :("
no_events_to_unsubscribe_msg: str = "No events to unsubscribe from :("
events_to_subscribe_msg: str = "Events to subscribe to:"
events_to_unsubscribe_msg: str = "Events to unsubscribe from:"
event_subscription_msg: str = "You successfully subscribed to <event>"
event_unsubscription_msg: str = "You successfully unsubscribed from <event>"
already_subscibed_msg: str = "You already subscribed <event>"
already_unsubscibed_msg: str = "You never subscribed <event>"

# commands
no_commands_msg: str = "no commands for you :("
commands_msg: str = "You can execute the following commands:"
unknown_command_msg: str = "I do not know the command \"<command>\"..."
command_suggestion_msg: str = "Did you mean <command>?"
command_400: str = "The command does not work like that."

# ban user
ban_msg: str = "You are not welcome here! You have been banned!"
ban_notification: str = "You have been banned! You wont be able to interact with me anymore."
unban_notification: str = "You have been unbanned. You can now talk to me again."
ban_user_400_msg: str = "Usage:\nType the command, the username you want to ban / unban space separated"
already_banned_msg: str = "<user> is already banned"
not_banned_yet_msg: str = "<user> was never banned"
banned_msg: str = "Successfully banned <user>"
unbanned_msg: str = "Successfully unbanned <user>"
no_admin_ban_msg: str = "<user> is admin, you cannot ban admins"

# permit user
permit_user_400_msg: str = "Usage:\nType the command, the username you want to permit and the permission you want to" \
                           " grant / ungrant all space separated"
unknown_permission_msg: str = "Permission <permission> does not exist"
permission_notification: str = "You have been permitted '<permission>' :)"
unpermission_notification: str = "You have been unpermitted '<permission>' :("
user_already_permitted_msg: str = "<user> is already permitted for <permission>"
user_not_permitted_yet_msg: str = "<user> never was permitted for <permission>"
user_permitted_msg: str = "Successfully permitted <user> to <permission>"
user_unpermitted_msg: str = "Successfully unpermitted <user> to <permission>"

# general
unknown_user_msg: str = "unknown user \"<user>\""
unknown_message_msg: str = "I do not know what to do with \"<message>\""
fact_msg: str = "Here is something you might have not known:\n\"<fact>\""
greeting_msg: str = "Hi, this is my telegram bot. I hope you like it. If you want access and should get one, " \
                    "you know where to find me"

# permission
not_permitted_msg: str = "You are not permitted to do so..."
no_username_msg: str = "You have to have a username to communicate with me"

# statistics
statistic_msg: str = f"User:\n" \
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
start_command_description: str = "Welcomes the user and introduces the bot"
help_command_description: str = "Shows a list of all available commands with their descriptions"
commands_command_description: str = "Shows a list of all available commands with their descriptions"
events_command_description: str = "Lists all events you can subscribe to"
my_events_command_description: str = "Lists all events you can unsubscribe from"
subscribe_command_description: str = "Lets you subscribe to an eventname. Type \"/sub <event_name>\""
subscribe_command_help = "Type \"/sub <event_name>\" and replace the <event_name> with the corresponding event. Type \"/events\" to list all available events to sub to"
unsubscribe_command_description: str = "Lets you unsubscribe from an eventname. Type \"/unsub <event_name>\""
unsubscribe_command_help = "Type \"/unsub <event_name>\" and replace the <event_name> with the corresponding event. Type \"/my_events\" to list all available events to unsub from"
permit_command_description: str = "Lets you permit a user to a specific permission level. Type \"/permit <username> <permission>\""
permit_command_help = "Type \"/permit <username> <permission>\""
unpermit_command_description: str = "Lets you unpermit a user to a specific permission level. Type \"/unpermit <username> <permission>\""
unpermit_command_help = "Type \"/unpermit <username> <permission>\""
ban_command_description: str = "Lets you ban a user so he cant interact with the bot whatsoever"
ban_command_help = "Type \"/ban <username>\" and replace the username by any name. You cannot ban admins. The banned user will be notified if he ever chatted with the bot"
unban_command_description: str = "Lets you unban a user so he can interact with the bot again"
unban_command_help = "Type \"/unban <username>\" and replace the username by any name. The user will be notified if he ever chatted with the bot"


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
            _msg = _msg.replace(f"<{_placeholder}>", str(value))

    return _msg
