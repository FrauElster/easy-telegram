from typing import Callable

from sqlalchemy.orm import Session, sessionmaker

from .singleton import singleton


class SessionHandler:
    __metaclass__ = singleton

    _session_cls: Callable[[], Session]
    _current_session: Session

    @property
    def session(self) -> Session:
        if not self._current_session._is_clean():  # pylint: disable=E1101,W0212 type: ignore
            self._current_session.commit()  # pylint: disable=E1101
        return self._current_session

    def __init__(self):
        from ..models import engine  # so that test db can monkey patch engine
        self._session_cls = sessionmaker(bind=engine)
        self._current_session = self._session_cls()
