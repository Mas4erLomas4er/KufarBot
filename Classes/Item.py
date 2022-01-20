class Item:
    def __init__(self, unparsed):
        self.unparsed = unparsed
        self.premium = self.check_premium()
        self.id = self.parse_id()
        self.title = self.parse_title()
        self.price = self.parse_price()

    def check_premium(self):
        return len(self.unparsed.select('.kf-Tbrz-ffe9e')) > 0

    def parse_id(self):
        try:
            return self.unparsed.select('.kf-TbTm-0178f')[0]['href'][-9:]
        except IndexError:
            return 0

    def parse_title(self):
        try:
            return self.unparsed.select('.kf-TbAJ-ac736')[0].text
        except IndexError:
            return "Unable to get title"

    def parse_price(self):
        try:
            return self.unparsed.select('.kf-TbHW-7ea75 span')[0].text
        except IndexError:
            return "Unable to get price"

    def stringify(self):
        return f'Title: {self.title}\nPrice: {self.price}\nLink: https://www.kufar.by/item/{self.id}'