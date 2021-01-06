from copy import copy
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Union, List, Tuple

from telegram import ReplyMarkup, MessageEntity, Bot, ChatAction
from telegram.ext import Handler, MessageHandler, Filters, CommandHandler
from telegram.utils.types import JSONDict

from easy_telegram import get_env
from easy_telegram.base_commands.unknown_message import unknown_message
from easy_telegram.bot.BotMode import BotMode
from easy_telegram.bot.access_check import access_check
from easy_telegram.bot.bot import TelegramBot
from easy_telegram.bot.send_action import send_action
from easy_telegram.bot.username_check import username_check
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


class BotSendDoc(Exception):
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
    text: str
    message_id: int = field(default_factory=FACTORY.get_msg_id)
    chat_id: int = field(default_factory=FACTORY.get_chat_id)
    date: datetime = field(default_factory=datetime.now)
    from_user: MockUser = field(default_factory=MockUser)
    forward_from: Optional[MockUser] = None
    forward_from_message_id: Optional[int] = None
    forward_date: Optional[datetime] = None
    reply_to_message: 'MockMessage' = None
    edit_date: datetime = None


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

    def send_document(self,
                      chat_id: Union[int, str],
                      document: str):
        assert chat_id is not None, "chat_id is non-optional"
        assert document is not None, "document is non-optional"
        raise BotSend(document)


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
            # should handler take it
            if isinstance(handler, CommandHandler):
                cmd = update.message.text.split(" ")[0]
                if cmd[0] == "/" and cmd[1:] == handler.command[0]:
                    cp_update = copy(update)
                    cp_update.message.text = cp_update.message.text[1:]
                    handler.callback(cp_update, context)
            elif isinstance(handler, MessageHandler):
                handler.callback(update, context)
            else:
                raise ValueError(f"unmocked handler {handler}")


def bot_init(self, token: str = None, mode: BotMode = BotMode.WHITELIST,
             admin_names: List[str] = None, whitelist_names: List[str] = None) -> TelegramBot:
    self.mode = mode

    if admin_names is None:
        admin_names = []
    admin_names.extend(get_env("TELEGRAM_ADMIN", type_=str, default="").split(" "))
    self._setup_admins(admin_names)

    if whitelist_names is None:
        whitelist_names = []
    whitelist_names.extend(get_env("TELEGRAM_WHITELIST", type_=str, default="").split(" "))
    self._setup_whitelist(whitelist_names)
    self._dispatcher = MockDispatcher()
    self._unknown_msg_handler = self._unknown_msg_handler = MessageHandler(Filters.text, send_action(ChatAction.TYPING)(
        username_check(access_check()(unknown_message))))
    self._dispatcher.add_handler(self._unknown_msg_handler)

    self._add_commands()


def bot_send_message(self,
                     chat_id: Union[int, str],
                     text: str):
    raise BotSend(text)


def bot_send_document(self,
                      chat_id: str,
                      document: str,
                      caption: str = None):
    raise BotSendDoc(document)
