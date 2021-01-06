# easy-telegram

This is a high-level api on top of [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).
It allows you to easily create a bot, add Commands and Events and have it run in whitelist or blacklist mode.

## disclaimer - pre-alpha

Well this project somewhat works and is somewhat tested, but not yet documented and stuff.
Also it is not tested too well and I also plan on adding some features.

Furthermore I have to add examples, and installation guides ands so on.

But I want to use it at work and implement it there as a pypy package, therefore I am going to publish it rn, even tho it it "pre-alpha".

I am planning on further working on it, but not today and not this week.

## Env vars

_TELEGRAM_ADMIN_ - space separated list of usernames
_TELEGRAM_WHITELIST_ - space separated list of usernames
_TELEGRAM_TOKEN_ - the bot token
_TELEGRAM_DB_FILE_ - the file for the db (optional)
_TELEGRAM_LOG_DIR_ - the log dir (optional)

## Commands and Events

These are the two main ways to communicate / interact with your bot. A command is an action provoked by the user, as one would think.
It can have permissions and do various things. There are some build in commands, like subscribe/unsubscribe to events, permit/ban users, ...

Events are event base things, say your code crawls a website and checks for something to happen, e.g. lower price on a project,
than you can trigger an event that notifies all users that subscribed to it.

