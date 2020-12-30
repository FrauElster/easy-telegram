import pytest

from tests.Mock import BotSend, MockBot
from tests.Randomizer import Randomizer


class TestEssentials:
    def test_mock_bot(self):
        bot = MockBot()
        randomizer = Randomizer()
        msg_text = "Hello World"
        with pytest.raises(BotSend) as msg:
            bot.send_message(chat_id=randomizer.random_int(1000, 9999), text=msg_text)
            assert msg.value == msg_text
