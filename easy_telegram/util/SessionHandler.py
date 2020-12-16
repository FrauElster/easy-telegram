from typing import Callable

from sqlalchemy.orm import Session, sessionmaker

from .singleton import singleton
from ..models import engine


class SessionHandler:
    __metaclass__ = singleton

    _session_cls: Callable[[], Session]
    _current_session: Session

    @property
    def session(self) -> Session:
        if not self._current_session._is_clean():
            self._current_session.commit()
        return self._current_session

    def __init__(self):
        self._session_cls = sessionmaker(bind=engine)
        self._current_session = self._session_cls()

