from typing import Optional, Callable

from telegram import ChatAction, Update
from telegram.ext import Updater, Dispatcher, MessageHandler, CommandHandler, Filters, CallbackContext

from easy_telegram.base_commands.unknown_message import unknown_message
from easy_telegram.bot.access_check import access_check
from easy_telegram.bot.arg_check import arg_check
from easy_telegram.bot.send_action import send_action
from easy_telegram.bot.username_check import username_check
from easy_telegram.models.Command import Command
from easy_telegram.util.utils import get_logger
from easy_telegram.util.State import State
from easy_telegram.util.StoppableThread import StoppableThread
from easy_telegram.util.utils import get_env


class TelegramBot:
    _logger = get_logger("TelegramBot")

    _dispatcher: Dispatcher
    _updater: Updater
    _unknown_msg_handler: MessageHandler

    _background_thread: Optional[StoppableThread]

    def __init__(self):
        self._updater = Updater(token=get_env("TELEGRAM_TOKEN", type_=str), use_context=True)
        self._dispatcher = self._updater.dispatcher

        self._unknown_msg_handler = self._unknown_msg_handler = MessageHandler(Filters.text, unknown_message)
        self._dispatcher.add_handler(self._unknown_msg_handler)

        self._add_commands()

        self._start_background_thread()

    def reload(self):
        self._background_thread.stop()
        self._dispatcher.handlers.clear()
        self._dispatcher.add_handler(self._unknown_msg_handler)
        self._add_commands()

    def _add_commands(self):
        for command in State().commands:
            command_callback = self._wrap_command(command)
            self._dispatcher.add_handler(CommandHandler(command.name, command_callback))

        # put the unknown message handler as last handler
        self._dispatcher.remove_handler(self._unknown_msg_handler)
        self._dispatcher.add_handler(self._unknown_msg_handler)

    @staticmethod
    def _wrap_command(command: Command) -> Callable[[Update, CallbackContext], None]:
        """
        Wraps the callback with various enrichment wrappers, such as access_check, stats or send_action

        The following instructions are wrappers and will be executed from outer-most to inner-most.
        Therefore one has to read them in reverse, so the first line of code ('command_callback = command.callback') is
        executed last.
        The order matters, because some wrappers depend on others. So the access_check requires the user to have a username set,
        therefore the username_check has to be executed before.
        :param command: the Command to wrap
        :return: the wrapped, enriched callback function of the command
        """
        command_callback = command.callback
        command_callback = arg_check(command.args_number, command.help_usage)(command_callback)
        command_callback = access_check(command.permissions)(command_callback)
        command_callback = username_check(command_callback)
        command_callback = send_action(ChatAction.TYPING)(command_callback)

        return command_callback  # type: ignore

    def _start_background_thread(self):
        self._background_thread = StoppableThread(target=self._updater.start_polling,
                                                  name="telegram_polling")
        self._background_thread.setDaemon(True)
        self._background_thread.start()
