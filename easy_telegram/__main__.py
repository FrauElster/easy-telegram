from time import sleep

from .bot.bot import TelegramBot


def main():
    TelegramBot()

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
