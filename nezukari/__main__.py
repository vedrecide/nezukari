from nezukari.core.bot import Bot
from nezukari.core.client import Client

if __name__ == '__main__':
    bot = Bot()
    (
        Client.from_gateway_bot(bot)
        ._load_modules()
    )
    bot.run()
