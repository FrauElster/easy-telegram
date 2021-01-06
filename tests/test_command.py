import pytest
from telegram import Update
from telegram.ext import CallbackContext

from easy_telegram.base_commands.messages import COMMAND_400, NOT_PERMITTED_MESSAGE
from easy_telegram.bot.BotMode import BotMode
from easy_telegram.bot.bot import TelegramBot
from easy_telegram.models.Command import Command
from easy_telegram.models.Permission import Permission
from easy_telegram.models.User import User
from tests.Mock import MockMessage, MockUpdate, BotSend, MockUser
from tests.common import receive_msg

SEND_TEXT = "test command called"
SEND_DOC = "test document called"


def send_text(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text=SEND_TEXT)


def send_document(update: Update, context: CallbackContext):
    context.bot.send_document(chat_id=update.message.chat_id, document=SEND_DOC)


class TestCommand:
    def test_command(self):
        Command("test", "test command", callback=send_text)
        bot = TelegramBot(mode=BotMode.BLACKLIST)

        msg = MockMessage(text="/test")
        update = MockUpdate(message=msg)

        with pytest.raises(BotSend) as e_info:
            receive_msg(bot, update)

        bots_message = str(e_info.value)
        assert bots_message == SEND_TEXT

    def test_command_with_args(self):
        Command("test_args", "test command with arguments", callback=send_text, args_number=2)
        bot = TelegramBot(mode=BotMode.BLACKLIST)

        msg_no_args = MockMessage(text="/test_args")
        msg_wrong_args = MockMessage(text="/test_args one")
        msg_right_args = MockMessage(text="/test_args one two")

        update = MockUpdate(message=msg_no_args)
        with pytest.raises(BotSend) as e_info:
            receive_msg(bot, update)
        bots_message = str(e_info.value)
        assert bots_message == COMMAND_400

        update = MockUpdate(message=msg_wrong_args)
        with pytest.raises(BotSend) as e_info:
            receive_msg(bot, update)
        bots_message = str(e_info.value)
        assert bots_message == COMMAND_400

        update = MockUpdate(message=msg_right_args)
        with pytest.raises(BotSend) as e_info:
            receive_msg(bot, update)
        bots_message = str(e_info.value)
        assert bots_message == SEND_TEXT

    def test_command_with_help(self):
        help_text = "This is the help message"
        Command("test_help", "test command with help", callback=send_text, help_usage=help_text)
        bot = TelegramBot(mode=BotMode.BLACKLIST)

        msg = MockMessage(text="/help")

        update = MockUpdate(message=msg)
        with pytest.raises(BotSend) as e_info:
            receive_msg(bot, update)
        bots_message = str(e_info.value)
        assert help_text in bots_message

    def test_command_with_perm(self):
        admin_perm = Permission.get_or_create(name="admin")
        Command("test_perm", "test command with permission", callback=send_text, permissions=[admin_perm])
        bot = TelegramBot(mode=BotMode.BLACKLIST, admin_names=["admin_user"])

        msg = MockMessage(text="/test_perm")
        msg_admin = MockMessage(text="/test_perm", from_user=MockUser(username="admin_user"))

        update = MockUpdate(message=msg)
        with pytest.raises(BotSend) as e_info:
            receive_msg(bot, update)
        bots_message = str(e_info.value)
        assert bots_message == NOT_PERMITTED_MESSAGE

        update = MockUpdate(message=msg_admin)
        with pytest.raises(BotSend) as e_info:
            receive_msg(bot, update)
        bots_message = str(e_info.value)
        assert bots_message == SEND_TEXT
