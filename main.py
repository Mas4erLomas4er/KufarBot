import asyncio

import config as config
import async_helper
from Classes.Bot import Bot


def run():
    async_helper.loop = asyncio.new_event_loop()
    b = Bot(config.TOKEN)


if __name__ == '__main__':
    run()
