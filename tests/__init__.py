TEST_DB = "test.db"


def _db_setup():
    import os
    import atexit
    if os.path.isfile(TEST_DB):
        os.remove(TEST_DB)
    atexit.register(os.remove, TEST_DB)

    from sqlalchemy import create_engine
    import easy_telegram.models
    easy_telegram.models.engine = create_engine(f'sqlite:///{TEST_DB}')
    easy_telegram.models.Base.metadata.create_all(easy_telegram.models.engine)


_db_setup()

from easy_telegram.bot.bot import TelegramBot
from tests.Mock import bot_init

TelegramBot.__init__ = bot_init
