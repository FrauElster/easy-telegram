from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Union, List, Tuple

from telegram import ReplyMarkup, MessageEntity, Bot
from telegram.ext import Handler, MessageHandler, Filters
from telegram.utils.types import JSONDict

from easy_telegram.base_commands.unknown_message import unknown_message
from easy_telegram.bot.bot import TelegramBot
from tests.Randomizer import Randomizer


class _Factory:
    user_rand: Randomizer
    msg_rand: Randomizer
    update_rand: Randomizer
    bot_rand: Randomizer
    chat_rand: Randomizer

    def __init__(self):
        self.bot_rand = Randomizer()
        self.user_rand = Randomizer()
        self.update_rand = Randomizer()
        self.msg_rand = Randomizer()
        self.chat_rand = Randomizer()

    def get_user_id(self) -> int:
        return self.user_rand.random_int(10000, 99999, unique=True)

    def get_user_first_name(self) -> str:
        return self.user_rand.first_name()

    def get_user_last_name(self) -> str:
        return self.user_rand.last_name()

    def get_user_user_name(self) -> str:
        return self.user_rand.first_name(unique=True)

    def get_msg_id(self) -> int:
        return self.msg_rand.random_int(10000, 99999, unique=True)

    def get_chat_id(self) -> int:
        return self.msg_rand.random_int(10000, 99999, unique=True)

    def get_update_id(self) -> int:
        return self.update_rand.random_int(10000, 99999, unique=True)

    def get_bot_id(self) -> int:
        return self.bot_rand.random_int(10000, 99999, unique=True)

    def get_bot_token(self) -> str:
        return self.bot_rand.random_str(128, unique=True)


FACTORY = _Factory()


class BotSend(Exception):
    pass


@dataclass
class MockUser:
    id: int = field(default_factory=FACTORY.get_user_id)
    first_name: Optional[str] = field(default_factory=FACTORY.get_user_first_name)
    last_name: Optional[str] = field(default_factory=FACTORY.get_user_last_name)
    username: Optional[str] = field(default_factory=FACTORY.get_user_user_name)
    is_bot: bool = False

    def __getitem__(self, item):
        if item not in self.__class__.__dict__['__annotations__'].keys():
            raise IndexError(f'{item} is not a attribute of {self.__class__.__name__}')
        return self.__getattribute__(item)


@dataclass
class MockMessage:
    message_id: int = field(default_factory=FACTORY.get_msg_id)
    chat_id: int = field(default_factory=FACTORY.get_chat_id)
    date: datetime = field(default_factory=datetime.now)
    from_user: MockUser = field(default_factory=MockUser)
    forward_from: Optional[MockUser] = None
    forward_from_message_id: Optional[int] = None
    forward_date: Optional[datetime] = None
    reply_to_message: 'MockMessage' = None
    edit_date: datetime = None
    text: str = None


@dataclass
class MockBot:
    token: str = field(default_factory=FACTORY.get_bot_token)
    last_chat_action_sent: Optional[str] = None

    def send_chat_action(self, chat_id: Union[str, int], action: str, timeout: float = None,
                         api_kwargs: JSONDict = None):
        self.last_chat_action_sent = action

    def send_message(self,
                     chat_id: Union[int, str],
                     text: str,
                     parse_mode: str = None,
                     disable_web_page_preview: bool = None,
                     disable_notification: bool = False,
                     reply_to_message_id: Union[int, str] = None,
                     reply_markup: ReplyMarkup = None,
                     timeout: float = None,
                     api_kwargs: JSONDict = None,
                     allow_sending_without_reply: bool = None,
                     entities: Union[List[MessageEntity], Tuple[MessageEntity, ...]] = None, ):
        assert chat_id is not None, "chat_id is non-optional"
        assert text is not None, "text is non-optional"
        raise BotSend(text)


@dataclass
class MockUpdate:
    update_id: int = field(default_factory=FACTORY.get_update_id)
    message: MockMessage = field(default_factory=MockMessage)


@dataclass
class MockContext:
    bot: MockBot = field(default_factory=MockBot)

    @staticmethod
    def from_update(update: MockUpdate) -> 'MockContext':
        return MockContext()


@dataclass
class MockDispatcher:
    handlers: List[Handler] = field(default_factory=list)

    def add_handler(self, handler: Handler):
        assert handler not in self.handlers
        self.handlers.append(handler)

    def remove_handler(self, handler: Handler):
        assert handler in self.handlers
        self.handlers.remove(handler)

    def process_update(self, update: MockUpdate):
        context = MockContext.from_update(update)
        for handler in self.handlers:
            handler.callback(update, context)


def bot_init(self) -> TelegramBot:
    self._dispatcher = MockDispatcher()
    self._unknown_msg_handler = self._unknown_msg_handler = MessageHandler(Filters.text, unknown_message)
    self._dispatcher.add_handler(self._unknown_msg_handler)

    self._add_commands()
