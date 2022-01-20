import aiohttp
import asyncio

loop = asyncio.new_event_loop()


async def get(url, callback):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            return callback(await r.text())


def run(callback, *args):
    loop.create_task(callback(*args))
