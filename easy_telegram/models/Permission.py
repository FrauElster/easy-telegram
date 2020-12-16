from typing import Optional

from sqlalchemy import Column, String
from sqlalchemy.orm import Session
from sqlalchemy.sql import ClauseElement

from . import Base
from ..util.LoggerFactory import get_logger
from ..util.SessionHandler import SessionHandler


class Permission(Base):
    _logger = get_logger("Permission")

    name = Column(String, nullable=False, unique=True)

    @classmethod
    def get_or_create(cls, session: Optional[Session] = None, defaults=None, **kwargs):
        if session is None:
            session = SessionHandler().session
        instance = session.query(cls).filter_by(**kwargs).first()
        if instance:
            cls._logger.debug("Found instance of %s in db", cls.__name__)
            return instance
        else:
            params = {k: v for k, v in kwargs.items() if not isinstance(v, ClauseElement)}
            params.update(defaults or {})
            instance = cls(**params)
            session.add(instance)
            session.commit()
            cls._logger.debug("Created new instance of %s in db", cls.__name__)
            return instance

    @classmethod
    def exists(cls, **kwargs) -> bool:
        session = SessionHandler().session
        instance = session.query(cls).filter_by(**kwargs).first()
        return instance is not None
