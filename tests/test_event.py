import pytest

from easy_telegram.base_commands.messages import get_msg, UNKNOWN_EVENT_MSG, NO_EVENTS_TO_SUBSCRIBE_MSG, \
    EVENT_SUBSCRIPTION_MSG, ALREADY_SUBSCRIBED_MSG, EVENT_UNSUBSCRIPTION_MSG, ALREADY_UNSUBSCRIBED_MSG
from easy_telegram.bot.BotMode import BotMode
from easy_telegram.bot.bot import TelegramBot
from easy_telegram.models.Event import Event
from tests.Mock import MockMessage, MockUpdate, BotSend, MockUser
from tests.common import receive_msg


class TestEvent:
    def test_creation_deletion(self):
        event = Event.get_or_create(name="TestEvent", description="basic test event")
        assert Event.exists(name="TestEvent")

        event.delete()
        assert not Event.exists(name="TestEvent")

    def test_listing(self):
        # test no event listing
        bot = TelegramBot(mode=BotMode.BLACKLIST)
        msg = MockMessage(text="/events")
        update = MockUpdate(message=msg)
        with pytest.raises(BotSend) as e_info:
            receive_msg(bot, update)
        bots_message = str(e_info.value)
        assert bots_message == NO_EVENTS_TO_SUBSCRIBE_MSG

        Event.get_or_create(name="TestEvent", description="basic test event")

        # test event listing
        msg = MockMessage(text="/events")
        update = MockUpdate(message=msg)
        with pytest.raises(BotSend) as e_info:
            receive_msg(bot, update)
        bots_message = str(e_info.value)
        assert "TestEvent" in bots_message

    def test_sub(self):
        bot = TelegramBot(mode=BotMode.BLACKLIST)
        event = Event.get_or_create(name="TestEvent", description="basic test event")

        # test unknown event
        msg = MockMessage(text="/sub monty")
        update = MockUpdate(message=msg)
        with pytest.raises(BotSend) as e_info:
            receive_msg(bot, update)
        bots_message = str(e_info.value)
        assert bots_message == get_msg(UNKNOWN_EVENT_MSG)

        user = MockUser()

        # test premature unsub
        msg = MockMessage(text="/unsub TestEvent", from_user=user)
        update = MockUpdate(message=msg)
        with pytest.raises(BotSend) as e_info:
            receive_msg(bot, update)
        bots_message = str(e_info.value)
        assert bots_message == get_msg(ALREADY_UNSUBSCRIBED_MSG, {"event": "TestEvent"})

        # test sub
        msg = MockMessage(text="/sub TestEvent", from_user=user)
        update = MockUpdate(message=msg)
        with pytest.raises(BotSend) as e_info:
            receive_msg(bot, update)
        bots_message = str(e_info.value)
        assert bots_message == get_msg(EVENT_SUBSCRIPTION_MSG, {"event": "TestEvent"})
        event = Event.get_or_create(name="TestEvent")  # has to be renewed to not be lazy instance call
        assert update.message.from_user.username in map(lambda user: user.name, event.subscribers)

        # test sub duplicate
        msg = MockMessage(text="/sub TestEvent", from_user=user)
        update = MockUpdate(message=msg)
        with pytest.raises(BotSend) as e_info:
            receive_msg(bot, update)
        bots_message = str(e_info.value)
        assert bots_message == get_msg(ALREADY_SUBSCRIBED_MSG, {"event": "TestEvent"})
        event = Event.get_or_create(name="TestEvent")  # has to be renewed to not be lazy instance call
        assert update.message.from_user.username in map(lambda user: user.name, event.subscribers)

        # test unsub listing
        msg = MockMessage(text="/my_events", from_user=user)
        update = MockUpdate(message=msg)
        with pytest.raises(BotSend) as e_info:
            receive_msg(bot, update)
        bots_message = str(e_info.value)
        assert "TestEvent" in bots_message

        # test unsub
        msg = MockMessage(text="/unsub TestEvent", from_user=user)
        update = MockUpdate(message=msg)
        with pytest.raises(BotSend) as e_info:
            receive_msg(bot, update)
        bots_message = str(e_info.value)
        assert bots_message == get_msg(EVENT_UNSUBSCRIPTION_MSG, {"event": "TestEvent"})
        event = Event.get_or_create(name="TestEvent")  # has to be renewed to not be lazy instance call
        assert update.message.from_user.username not in map(lambda user: user.name, event.subscribers)
