from urllib3 import PoolManager as PM
from urllib.request import quote, unquote
import certifi
import numpy as np
from bs4 import BeautifulSoup as bs
import re
import os
from .gamerescape_parser import Parser

BASE = 'https://ffxiv.gamerescape.com/wiki/'


class Crawler:
    """
    TODO
    database > stored html
    store patch (or maybe just date) entry was fetched
    update if outdated
    """

    def __init__(self):
        self.pm = PM(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where()
        )
        self.save_base = 'html_files/'
        if not os.path.exists(self.save_base):
            os.mkdir(self.save_base)

    def get_html(self, name):
        name = name.strip()
        name = name.title()
        print(name)
        name = name.replace(' ', '_')
        save_path = self.save_base + name + '.html'
        if os.path.exists(save_path):
            with open(save_path, 'r') as h:
                html = h.read().replace('''\\n''', '')
        else:
            url = 'https://ffxiv.gamerescape.com/wiki/' + name
            # url = '''https://ffxiv.gamerescape.com/w/index.php?title=Special%3ASearch&search={}&go=Go'''.format(quote(name))
            response = self.pm.request('GET', url)
            print(response.status)
            assert response.status == 200
            html = response.data
            with open(save_path, 'w') as h:
                h.write(str(html))

        return html

    def get_tables(self, name):
        html = self.get_html(name)
        soup = bs(html, 'html5lib')
        tables = soup.find_all(class_='mw-collapsible')
        results = []

        for table in tables:
            parser = Parser(table)
            data = parser.parse()
            results += [data]

        return results


