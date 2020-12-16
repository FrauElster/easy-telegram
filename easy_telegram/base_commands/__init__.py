from assests.messages import help_command_description, start_command_description, permit_command_description, \
    unpermit_command_description, ban_command_description, unban_command_description, subscribe_command_description, \
    unsubscribe_command_description, events_command_description, my_events_command_description, \
    commands_command_description, subscribe_command_help, unsubscribe_command_help, permit_command_help, \
    unpermit_command_help, ban_command_help, unban_command_help


def setup_base_commands():
    from easy_telegram.models.Command import Command
    from easy_telegram.base_commands.ban_command import ban_command
    from easy_telegram.base_commands.commands_command import commands_command
    from easy_telegram.base_commands.event_subscribe_commands import event_subscribe_command
    from easy_telegram.base_commands.event_unsubscribe_command import event_unsubscribe_command
    from easy_telegram.base_commands.permit_command import permit_command
    from easy_telegram.base_commands.start_command import start_command
    from easy_telegram.base_commands.subscribe_command import subscribe_command
    from easy_telegram.base_commands.unban_command import unban_command
    from easy_telegram.base_commands.unpermit_command import unpermit_command
    from easy_telegram.base_commands.unsubscribe_command import unsubscribe_command
    from easy_telegram.models.Permission import Permission

    admin_permission = Permission.get_or_create(name="admin")

    Command(name="start", description=start_command_description, callback=start_command)
    Command(name="help", description=help_command_description, callback=commands_command)
    Command(name="sub", description=subscribe_command_description, help_usage=subscribe_command_help,
            callback=subscribe_command, args_number=1)
    Command(name="unsub", description=unsubscribe_command_description,
            help_usage=unsubscribe_command_help, callback=unsubscribe_command, args_number=1)
    Command(name="events", description=events_command_description, callback=event_subscribe_command)
    Command(name="my_events", description=my_events_command_description, callback=event_unsubscribe_command)
    Command(name="commands", description=commands_command_description, callback=commands_command)

    Command(name="permit", description=permit_command_description, args_number=2,
            help_usage=permit_command_help, callback=permit_command, permissions=[admin_permission.name])
    Command(name="unpermit", description=unpermit_command_description, callback=unpermit_command,
            help_usage=unpermit_command_help, permissions=[admin_permission.name], args_number=2)
    Command(name="ban", description=ban_command_description, callback=ban_command,
            help_usage=ban_command_help, permissions=[admin_permission.name], args_number=1)
    Command(name="unban", description=unban_command_description, callback=unban_command,
            help_usage=unban_command_help, permissions=[admin_permission.name], args_number=1)
