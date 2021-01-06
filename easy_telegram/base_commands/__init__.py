from easy_telegram.base_commands.help_command import help_command
from easy_telegram.base_commands.messages import HELP_COMMAND_DESCRIPTION, START_COMMAND_DESCRIPTION, PERMIT_COMMAND_DESCRIPTION, \
    UNPERMIT_COMMAND_DESCRIPTION, BAN_COMMAND_DESCRIPTION, UNBAN_COMMAND_DESCRIPTION, SUBSCRIBE_COMMAND_DESCRIPTION, \
    UNSUBSCRIBE_COMMAND_DESCRIPTION, EVENTS_COMMAND_DESCRIPTION, MY_EVENTS_COMMAND_DESCRIPTION, \
    COMMANDS_COMMAND_DESCRIPTION, SUBSCRIBE_COMMAND_HELP, UNSUBSCRIBE_COMMAND_HELP, PERMIT_COMMAND_HELP, \
    UNPERMIT_COMMAND_HELP, BAN_COMMAND_HELP, UNBAN_COMMAND_HELP


def setup_base_commands():
    from easy_telegram.models.Command import Command  # pylint: disable=C0415
    from easy_telegram.base_commands.ban_command import ban_command  # pylint: disable=C0415
    from easy_telegram.base_commands.commands_command import commands_command  # pylint: disable=C0415
    from easy_telegram.base_commands.event_subscribe_commands import event_subscribe_command  # pylint: disable=C0415
    from easy_telegram.base_commands.event_unsubscribe_command import event_unsubscribe_command  # pylint: disable=C0415
    from easy_telegram.base_commands.permit_command import permit_command  # pylint: disable=C0415
    from easy_telegram.base_commands.start_command import start_command  # pylint: disable=C0415
    from easy_telegram.base_commands.subscribe_command import subscribe_command  # pylint: disable=C0415
    from easy_telegram.base_commands.unban_command import unban_command  # pylint: disable=C0415
    from easy_telegram.base_commands.unpermit_command import unpermit_command  # pylint: disable=C0415
    from easy_telegram.base_commands.unsubscribe_command import unsubscribe_command  # pylint: disable=C0415
    from easy_telegram.models.Permission import Permission  # pylint: disable=C0415

    admin_permission = Permission.get_or_create(name="admin")

    Command(name="start", description=START_COMMAND_DESCRIPTION, callback=start_command)
    Command(name="help", description=HELP_COMMAND_DESCRIPTION, callback=help_command)
    Command(name="sub", description=SUBSCRIBE_COMMAND_DESCRIPTION, help_usage=SUBSCRIBE_COMMAND_HELP,
            callback=subscribe_command, args_number=1)
    Command(name="unsub", description=UNSUBSCRIBE_COMMAND_DESCRIPTION,
            help_usage=UNSUBSCRIBE_COMMAND_HELP, callback=unsubscribe_command, args_number=1)
    Command(name="events", description=EVENTS_COMMAND_DESCRIPTION, callback=event_subscribe_command)
    Command(name="my_events", description=MY_EVENTS_COMMAND_DESCRIPTION, callback=event_unsubscribe_command)
    Command(name="commands", description=COMMANDS_COMMAND_DESCRIPTION, callback=commands_command)

    Command(name="permit", description=PERMIT_COMMAND_DESCRIPTION, args_number=2,
            help_usage=PERMIT_COMMAND_HELP, callback=permit_command, permissions=[admin_permission.name])
    Command(name="unpermit", description=UNPERMIT_COMMAND_DESCRIPTION, callback=unpermit_command,
            help_usage=UNPERMIT_COMMAND_HELP, permissions=[admin_permission.name], args_number=2)
    Command(name="ban", description=BAN_COMMAND_DESCRIPTION, callback=ban_command,
            help_usage=BAN_COMMAND_HELP, permissions=[admin_permission.name], args_number=1)
    Command(name="unban", description=UNBAN_COMMAND_DESCRIPTION, callback=unban_command,
            help_usage=UNBAN_COMMAND_HELP, permissions=[admin_permission.name], args_number=1)
