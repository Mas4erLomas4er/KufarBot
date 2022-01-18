import time

import requests
from bs4 import BeautifulSoup
from .Item import Item


class Watcher:
    def __init__(self, link, event):
        self.link = link
        self.current = set()
        self.go = False
        self.event = event

    def start_watching(self, interval):
        self.current = self.check()

        self.go = True
        while self.go:
            res = self.get_updates()
            for el in res:
                item = Item(el)
                self.event(item.stringify())
            time.sleep(interval)

    def stop_watching(self):
        self.go = False

    def get_updates(self):
        new = self.check()
        res = set()
        for el in new:
            if not (el in self.current):
                res.add(el)
        self.current = new
        return res

    def check(self):
        r = requests.get(self.link)
        html = BeautifulSoup(r.content, 'html.parser')
        items_list = set()
        for el in reversed(html.select('.kf-aXXX-1c982 section')):
            if Item.check_premium(el):
                continue
            try:
                item_id = Item.get_id(el)
                items_list.add(item_id)
            except requests.RequestException:
                self.event('Unable to get item')

        return items_list
