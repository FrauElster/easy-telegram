from easy_telegram.bot.bot import TelegramBot
from tests.Mock import MockUpdate


def receive_msg(bot: TelegramBot, update: MockUpdate):
    bot._dispatcher.process_update(update)
