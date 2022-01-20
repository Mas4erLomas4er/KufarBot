import asyncio

import config as config
from Classes import Async
from Classes.Bot import Bot

Async.loop = asyncio.new_event_loop()
b = Bot(config.TOKEN)
