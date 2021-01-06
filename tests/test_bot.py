import pytest

from easy_telegram.base_commands.messages import NO_USERNAME_MSG, NOT_PERMITTED_MESSAGE
from easy_telegram.bot.bot import TelegramBot
from tests.Mock import MockUser, MockMessage, MockUpdate, BotSend
from tests.common import receive_msg


class TestBot:
    def test_no_username(self):
        bot = TelegramBot()
        user = MockUser(username=None)
        msg = MockMessage(from_user=user)
        update = MockUpdate(message=msg)

        with pytest.raises(BotSend) as e_info:
            receive_msg(bot, update)
        bots_message = str(e_info.value)
        assert bots_message == NO_USERNAME_MSG

    def test_no_whitelist(self):
        bot = TelegramBot()
        user = MockUser(username="hello_world")
        msg = MockMessage(from_user=user)
        update = MockUpdate(message=msg)

        with pytest.raises(BotSend) as e_info:
            receive_msg(bot, update)

        bots_message = str(e_info.value)
        assert bots_message == NOT_PERMITTED_MESSAGE
