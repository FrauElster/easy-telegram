import atexit
import logging
import os
import pathlib
import sys

PROJECT_ROOT = pathlib.Path(__file__).parent.parent.absolute()


def _check_version():
    if not (sys.version_info[0] >= 3 and sys.version_info[1] >= 7):
        raise Exception(
            f"Must be using Python 3.7 or newer, currently running {sys.version_info[0]}.{sys.version_info[1]}")
    print(f"Running with env: {sys.prefix} and python version: {sys.version_info[0]}.{sys.version_info[1]}")


def _load_env():
    _env_file = os.path.join(PROJECT_ROOT, ".env")
    if not os.path.isfile(_env_file):
        print(f".env file not found ('{_env_file}')")
        sys.exit(-1)
    from dotenv import load_dotenv  # pylint: disable=C0415
    load_dotenv(dotenv_path=_env_file, verbose=True)


_check_version()
from .util.utils import get_env  # pylint: disable=C0415,C0413

if get_env("TELEGRAM_DEBUG", type_=bool, default=False):
    _load_env()

DB_FILE = get_env('TELEGRAM_DB_FILE', type_=str, default=os.path.join(PROJECT_ROOT, "easy-telegram.db"))


def _logger_setup():
    LOG_DIR = get_env('TELEGRAM_LOG_DIR', type_=str, default=os.path.join(PROJECT_ROOT, "logs"))
    if not os.path.isdir(LOG_DIR):
        os.mkdir(LOG_DIR)

    rootLogger = logging.getLogger()
    if get_env("TELEGRAM_DEBUG", type_=bool, default=False):
        rootLogger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s \t|%(asctime)s \t| %(name)s \t|  %(message)s')

    console_handler: logging.StreamHandler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(os.path.join(LOG_DIR, f"telegram.{rootLogger.level}.log"))
    file_handler.setFormatter(formatter)

    rootLogger.addHandler(console_handler)
    rootLogger.addHandler(file_handler)



def _setup_db():
    from .util.SessionHandler import SessionHandler  # pylint: disable=C0415
    atexit.register(SessionHandler().session.commit)  # pylint: disable=E1101
    if os.path.isfile(DB_FILE):
        return
    from .models import Base, engine  # pylint: disable=C0415
    from .models.Permission import Permission  # pylint: disable=C0415
    from .models.User import User  # pylint: disable=C0415
    from .models.Event import Event  # noqa: F401  # pylint: disable=C0415,W0611
    from .models.event_subscriber import event_subscriber  # noqa: F401  # pylint: disable=C0415,W0611
    from .models.event_permissions import event_permissions  # noqa: F401  # pylint: disable=C0415,W0611
    from .models.user_permissions import user_permissions  # noqa: F401  # pylint: disable=C0415,W0611

    Base.metadata.create_all(engine)


_logger_setup()
_setup_db()
from easy_telegram.base_commands import setup_base_commands  # noqa: E402  # pylint: disable=C0413,C0411

setup_base_commands()
