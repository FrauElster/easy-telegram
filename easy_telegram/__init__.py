import atexit
import os
import pathlib
import sys

from dotenv import load_dotenv


def _check_version():
    if not (sys.version_info[0] >= 3 and sys.version_info[1] >= 7):
        raise Exception(
            "Must be using Python 3.7 or newer, currently running {sys.version_info[0]}.{sys.version_info[1]}")
    print(f"Running with env: {sys.prefix} and python version: {sys.version_info[0]}.{sys.version_info[1]}")


_check_version()

PROJECT_ROOT = pathlib.Path(__file__).parent.parent.absolute()
SOURCE_ROOT = pathlib.Path(__file__).parent.absolute()
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
_db_file = os.path.join(PROJECT_ROOT, "easy-telegram.db")
_env_file = os.path.join(PROJECT_ROOT, ".env")


def _check_requirements():
    error = []
    if not os.path.isfile(_env_file):
        error.append(f".env file not found ('{_env_file}')")

    if error:
        print("\n".join(error))
        exit(-1)


def _logger_setup():
    if not os.path.isdir(LOG_DIR):
        os.mkdir(LOG_DIR)


def _setup_db():
    from .util.SessionHandler import SessionHandler
    atexit.register(SessionHandler().session.commit)
    if os.path.isfile(_db_file):
        return
    from .util.utils import get_env
    from .models import Base, engine
    from .models.Permission import Permission
    from .models.User import User
    from .models.Event import Event
    from .models.event_subscriber import event_subscriber
    from .models.event_permissions import event_permissions
    from .models.user_permissions import user_permissions

    Base.metadata.create_all(engine)

    session = SessionHandler().session
    admin_perm = Permission.get_or_create(session, name="admin")
    admin_names = get_env("TELEGRAM_ADMIN", type_=str, default="").split(" ")
    for admin_name in admin_names:
        session.add(User(name=admin_name, permissions=[admin_perm], whitelisted=True))
    session.commit()


_check_requirements()
_logger_setup()
load_dotenv(dotenv_path=_env_file, verbose=True)
_setup_db()
from easy_telegram.base_commands import setup_base_commands

setup_base_commands()
