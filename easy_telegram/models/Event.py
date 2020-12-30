from typing import List, Optional, Iterable

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import ClauseElement

from . import Base
from .Permission import Permission
from .event_permissions import event_permissions
from .event_subscriber import event_subscriber
from ..util.utils import get_logger
from ..util.SessionHandler import SessionHandler


class Event(Base):
    _logger = get_logger("Event")

    # __table_args__ = (CheckConstraint("regexp_like(name, r'\w')", name="namecheck"),)

    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    permissions: Iterable[Permission] = relationship("Permission", secondary=event_permissions)
    subscribers = relationship("User", secondary=event_subscriber)  # type: ignore

    def notify(self, message: str, files: List[str]):
        pass

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

    @classmethod
    def exists(cls, **kwargs) -> bool:
        session = SessionHandler().session
        instance = session.query(cls).filter_by(**kwargs).first()  # pylint: disable=E1101
        return instance is not None  # pylint: disable=E1101
