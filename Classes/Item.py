class Item:
    def __init__(self, unparsed):
        self.unparsed = unparsed
        self.premium = self.check_premium()
        self.id = self.parse_id()
        self.title = self.parse_title()
        self.price = self.parse_price()

    def check_premium(self):
        return len(self.unparsed.select('img')) == 2

    def parse_id(self):
        try:
            return self.unparsed.a['href'][-9:]
        except IndexError:
            return 0

    def parse_title(self):
        try:
            return self.unparsed.h3.string
        except IndexError:
            return "Unable to get title"

    def parse_price(self):
        try:
            return self.unparsed.h3.parent.p.span.string
        except IndexError:
            return "Unable to get price"

    def stringify(self):
        return f'Title: {self.title}\nPrice: {self.price}\nLink: https://www.kufar.by/item/{self.id}'
