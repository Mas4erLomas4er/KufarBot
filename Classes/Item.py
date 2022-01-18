import requests
from bs4 import BeautifulSoup


class Item:
    @staticmethod
    def get_id(unparsed):
        return unparsed.select('.kf-TbTm-0178f')[0]['href'][-9:]

    @staticmethod
    def check_premium(unparsed):
        return len(unparsed.select('.kf-Tbrz-ffe9e')) > 0

    def __init__(self, item_id):
        self.id = item_id
        self.unparsed = self.get_item()
        self.title = self.parse_title()
        self.price = self.parse_price()

    def get_item(self):
        r = requests.get(f'https://www.kufar.by/item/{self.id}')
        return BeautifulSoup(r.content, 'html.parser')

    def parse_title(self):
        try:
            return self.unparsed.select('h1')[0].text
        except IndexError:
            return "Unable to get title"

    def parse_price(self):
        try:
            return self.unparsed.select('div[itemprop=offers] span')[0].text
        except IndexError:
            return "Unable to get price"

    def stringify(self):
        return f'Title: {self.title}\nPrice: {self.price}\nLink: https://www.kufar.by/item/{self.id}'
