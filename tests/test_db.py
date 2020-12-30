import pytest

from easy_telegram.bot.bot import TelegramBot
from easy_telegram.models.User import User
from tests.Mock import MockUser, MockMessage, MockUpdate, BotSend
from tests.common import receive_msg


class TestDb:
    def test_user_creation(self):
        bot = TelegramBot()
        user = MockUser()
        username = user.username
        msg = MockMessage(from_user=user)
        update = MockUpdate(message=msg)

        with pytest.raises(BotSend):
            receive_msg(bot, update)

        assert User.exists(name=username)
