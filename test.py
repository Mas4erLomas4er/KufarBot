import time

import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.kufar.by/l?sort=lst.d&cur=BYR&size=42')
bs = BeautifulSoup(r.content, 'html.parser')

for el in bs.select('section')[1:]:
    title = el.h3.string
    price = el.h3.parent.p.string
    i = el.a['href'][-9:]
    print(i)
    print('________________')
