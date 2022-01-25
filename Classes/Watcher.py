import asyncio
from bs4 import BeautifulSoup

import config
import async_helper
from .Item import Item


class Watcher:
    def __init__(self, link, event):
        self.link = link
        self.current = set()
        self.go = False
        self.event = event

    async def start_watching(self, interval=config.INTERVAL):
        res = await self.check()
        self.current = set(el.id for el in res)
        self.go = True
        while self.go:
            res = await self.get_updates()
            for el in res:
                if not self.go:
                    break
                await self.event(el.stringify())
            await asyncio.sleep(interval)

    def stop_watching(self):
        self.go = False

    async def get_updates(self):
        new = await self.check()
        res = set()
        for el in new:
            if not (el.id in self.current):
                res.add(el)
        self.current = set(el.id for el in new)
        return res

    async def check(self):
        html = await async_helper.get(self.link, lambda r: BeautifulSoup(r, 'html.parser'))
        item_list = list()
        for el in reversed(html.select('section')[1:]):
            item = Item(el)
            if item.premium:
                continue
            item_list.append(item)
        return item_list
