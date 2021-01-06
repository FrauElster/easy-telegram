from logging import getLogger
from typing import List, Union, Set, Optional, Iterable

from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import ClauseElement

from . import Base
from .Command import Command
from .Event import Event
from .Permission import Permission
from .user_permissions import user_permissions
from ..util.SessionHandler import SessionHandler
from ..util.State import State


class User(Base):
    _logger = getLogger("User")

    name = Column(String, nullable=False, unique=True)
    blocked = Column(Boolean, nullable=False, default=False)
    whitelisted = Column(Boolean, nullable=False, default=False)
    chat_id = Column(String)
    permissions: Iterable[Permission] = relationship("Permission", secondary=user_permissions)

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
        instance = cls(**params)  # type: ignore
        session.add(instance)
        session.commit()
        cls._logger.debug("Created new instance of %s in db", cls.__name__)
        return instance

    def is_permitted(self, event_or_command: Union[Event, Command]) -> bool:
        assert isinstance(event_or_command, (Event, Command)), "has to be either of type 'Event' or 'Command'"

        if isinstance(event_or_command, Command):
            return self._is_permitted_command(event_or_command)
        return self._is_permitted_event(event_or_command)

    def _is_permitted_command(self, command: Command) -> bool:
        if not command.permissions:
            # command is not restricted
            return True
        if not self.permissions:
            # user has no permission at all
            self._logger.debug("User %s is not permitted to execute %s", self.name, command.name)
            return False

        perm_names: Set[Permission] = set(map(lambda perm_: perm_.name, self.permissions))
        for perm in command.permissions:
            if perm in perm_names:
                return True
        # not permitted
        self._logger.debug("User %s is not permitted to execute %s", self.name, command.name)
        return False

    def _is_permitted_event(self, event: Event) -> bool:
        if not event.permissions:
            # event is not restricted
            return True
        if not self.permissions:
            # user has no permission at all
            self._logger.info("User %s is not permitted to subscribe to %s", self.name, event.name)
            return False

        perm_ids: Set[Permission] = set(map(lambda perm_: perm_.id, self.permissions))
        for perm in event.permissions:
            if perm.id in perm_ids:
                return True
        # not permitted
        self._logger.info("User %s is not permitted to subscribe to %s", self.name, event.name)
        return False

    @property
    def commands(self) -> List[Command]:
        all_: Set[Command] = State().commands
        return list(filter(self.is_permitted, all_))

    @property
    def events(self) -> List[Event]:
        session = SessionHandler().session
        all_ = session.query(Event).all()  # pylint: disable=E1101
        return list(filter(self.is_permitted, all_))

    @property
    def subscribed_events(self) -> List[Event]:
        result: List[Event] = []
        for event in self.events:
            if event.subscribers is None:
                continue
            subscriber_ids = map(lambda sub: sub.id, event.subscribers)
            if self.id in subscriber_ids:
                result.append(event)
        return result

    @property
    def is_admin(self) -> bool:
        if self.permissions is None:
            return False
        return "admin" in map(lambda perm_: perm_.name, self.permissions)

    @classmethod
    def exists(cls, **kwargs) -> bool:
        session = SessionHandler().session
        instance = session.query(cls).filter_by(**kwargs).first()  # pylint: disable=E1101
        return instance is not None
