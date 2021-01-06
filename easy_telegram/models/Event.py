import os
from logging import getLogger
from typing import List, Optional, Iterable

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import ClauseElement
from telegram import Bot

from . import Base
from .event_permissions import event_permissions
from .event_subscriber import event_subscriber
from .. import get_env
from ..base_commands.messages import EVENT_TRIGGERED_MSG, get_msg, EVENT_DISPOSAL_MSG
from ..util.SessionHandler import SessionHandler


class Event(Base):
    _logger = getLogger("Event")

    # __table_args__ = (CheckConstraint("regexp_like(name, r'\w')", name="namecheck"),)

    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    deletion_message = Column(String)
    permissions: Iterable['Permission'] = relationship("Permission", secondary=event_permissions)
    subscribers: Iterable['User'] = relationship("User", secondary=event_subscriber)  # type: ignore
    token = Column(String, nullable=False)

    def notify(self, message: str = None, file_names: List[str] = None):
        if message is None:
            message = get_msg(EVENT_TRIGGERED_MSG, {"event": self.name})
        files = []
        if file_names is not None:
            for file_name in file_names:
                if not os.path.isfile(file_name):
                    self._logger.warning("Could not send file %s: FileNotFound", file_name)
                else:
                    files.append(file_name)
        bot = Bot(token=self.token)

        for subscriber in self.subscribers:
            if subscriber.chat_id:
                bot.send_message(chat_id=subscriber.chat_id, text=message)
                for file in files:
                    bot.send_document(subscriber.chat_id, file, caption=os.path.basename(file))

    @classmethod
    def get_or_create(cls, session: Optional[Session] = None, defaults=None, **kwargs):
        if session is None:
            session = SessionHandler().session
        instance = session.query(cls).filter_by(**kwargs).first()
        if instance:
            cls._logger.debug("Found instance of %s in db", cls.__name__)
            return instance
        params = {k: v for k, v in kwargs.items() if not isinstance(v, ClauseElement)}
        params.update(defaults or {})
        if "token" not in params:
            params["token"] = get_env("TELEGRAM_TOKEN", type_=str)
        instance = cls(**params)  # type: ignore
        session.add(instance)
        session.commit()
        cls._logger.debug("Created new instance of %s in db", cls.__name__)
        return instance

    @classmethod
    def exists(cls, **kwargs) -> bool:
        session = SessionHandler().session
        instance = session.query(cls).filter_by(**kwargs).first()  # pylint: disable=E1101
        return instance is not None  # pylint: disable=E1101

    def delete(self):
        message = get_msg(EVENT_DISPOSAL_MSG, {"event": self.name})
        if self.deletion_message:
            message = self.deletion_message

        bot = Bot(token=self.token)
        for subscriber in self.subscribers:
            if subscriber.chat_id:
                bot.send_message(subscriber.chat_id, message)

        session = SessionHandler().session
        session.query(self.__class__).filter_by(id=self.id).delete()
        session.commit()

    def __eq__(self, other):
        if not isinstance(other, Event):
            raise ValueError(f"Cannot compare Event and {type(other)}")
        return self.id == other.id