from urllib3 import PoolManager as PM
from urllib.request import quote, unquote
import certifi
import numpy as np
from bs4 import BeautifulSoup as bs
import re
import os
from .GamerEscapeParser import Parser, append_dict

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

    def capitalise_word(self, word):
        uncapitalised_words = ['to', 'from', 'with', 'and', 'as', 'that', 'like']
        word = word.lower()
        word = word if word in uncapitalised_words else str.capitalize(word)
        return word

    def get_html(self, name):
        name = name.strip()
        name = '_'.join([self.capitalise_word(word) for word in name.split(' ')])
        print(name)
        save_path = self.save_base + name + '.html'
        if os.path.exists(save_path):
            with open(save_path, 'r') as h:
                html = h.read().replace('''\\n''', '')
            retcode = 200
        else:
            url = 'https://ffxiv.gamerescape.com/wiki/' + name
            # url = '''https://ffxiv.gamerescape.com/w/index.php?title=Special%3ASearch&search={}&go=Go'''.format(quote(name))
            response = self.pm.request('GET', url)
            retcode = response.status
            print(response.status)
            html = response.data
            if retcode == 200:
                with open(save_path, 'w') as h:
                    h.write(str(html))
            else:
                return None, retcode
        html = str(html).replace('''\\n''', '')
        return html, retcode

    def merge_ventures(self, tables):
        new_table = []
        venture_table = []
        empty = True
        for t in tables:
            key = list(t.keys())[0]
            if 'venture' in key.lower():
                venture_table += [t]
                empty = False
            else:
                new_table += [t]

        venture_dict = {}
        for d in venture_table:
            for k, v in zip(d.keys(), d.values()):
                venture_dict[k] = v[list(v)[0]]

        venture_dict = {'Venture': venture_dict}

        return new_table if empty else new_table + [venture_dict]

    def get_tables(self, name):
        html, retcode = self.get_html(name)
        if retcode != 200:
            return [], retcode
        soup = bs(html, 'html5lib')
        tables = soup.find_all(class_='mw-collapsible')
        results = []

        for table in tables:
            parser = Parser(table)
            data = parser.parse()
            results += [data]

        results = [result for result in results if result is not None]
        # print(results)
        results = self.merge_ventures(results)
        # print(results)

        return results, retcode
