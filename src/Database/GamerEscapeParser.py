from urllib.request import quote, unquote
import unicodedata
import re
import string

DEBUG = False

PLACEHOLDER = {'this': ['just', 'text'], 'is': ['placeholder', 'sorry']}


def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def sanitize_string(text):
    text = str(text)
    text = re.sub(r'\\x\w*', '', text)
    return unicodedata.normalize('NFKC', text).replace('\\', '')


def append_dict(small, big):
    for key in small:
        val = small[key]
        if key not in big:
            big[key] = [val]
        else:
            big[key] += [val]


class Parser:
    @staticmethod
    def get_headers(tr):
        headers = [str(td.text).strip() for td in tr.find_all('th')]
        debug_print(headers)
        return headers

    @staticmethod
    def get_currency(currency, ele):
        currency = str(currency).lower()
        if currency == 'gil':
            return ''.join(list(ele.descendants)[-2:])
        # elif 'sky pirate spoil' in currency:
        #    return ' '.join([re.sub('[()]', '', s) for s in list(ele.stripped_strings) if not '<' in s])
        else:
            return None

    @staticmethod
    def parse_merchant(tds):
        headers = Parser.get_headers(tds[0])
        rows = {}
        table_rows = tds[0].table.tbody.find_all('tr')

        for row in table_rows[1:]:
            valid = True
            row_dict = {}
            for h, c in zip(headers, row.children):
                if h == 'Cost' or h == 'Price':
                    currency = c.a.get('title')
                    amount = Parser.get_currency(currency, c)
                    if amount is None:  # not yet implemented
                        valid = False
                        break
                    row_dict[h] = '{} {}'.format(currency, sanitize_string(amount))
                else:
                    row_dict[h] = sanitize_string(c.text)
            if valid:
                append_dict(row_dict, rows)

        debug_print(rows)
        return rows

    @staticmethod
    def desynthesis(tds):
        headers = Parser.get_headers(tds[0])
        debug_print(headers)
        return PLACEHOLDER
        # raise NotImplementedError

    @staticmethod
    def used_recipes(tds):
        headers = Parser.get_headers(tds[0])
        debug_print(headers)
        return PLACEHOLDER
        # raise NotImplementedError

    @staticmethod
    def used_quest(tds):
        headers = Parser.get_headers(tds[0])
        debug_print(headers)
        return PLACEHOLDER
        # raise NotImplementedError

    @staticmethod
    def used_leve(tds):
        headers = Parser.get_headers(tds[0])
        debug_print(headers)
        return PLACEHOLDER
        # raise NotImplementedError

    @staticmethod
    def harvest(tds):
        headers = Parser.get_headers(tds[0])
        rows = {}
        table_rows = tds[0].table.tbody.find_all('tr')

        for row in table_rows[1:]:
            valid = True
            row_dict = {}
            for h, c in zip(headers, row.children):
                text = sanitize_string(c.small.text).replace(')', ') ').replace(':', ': ')
                if '<img alt' in text:
                    text = sanitize_string(' '.join([q for q in c.small.stripped_strings if not '<img' in q]))

                text = text.replace('Tome of', '\nTome of')
                text = text.replace('Unspoiled', ' - Unspoiled - ')
                text = text.replace('Ephemeral', ' - Ephemeral - ')

                row_dict[h] = text
            if valid:
                append_dict(row_dict, rows)

        debug_print(rows)
        return rows

    @staticmethod
    def recipes(tds):
        return PLACEHOLDER
        headers = Parser.get_headers(tds[0])
        debug_print(headers)
        # print(items)

        for td in tds:
            trs = td.div.table.tbody.find_all('tr')
            for tr in trs:
                debug_print(tr)
            input()

    def __init__(self, table):
        self.table = table
        self.parse_dict = {
            'sold by merchant': self.parse_merchant,
            'reduction resulting': self.parse_merchant,
            'venture': self.parse_merchant,
            'harvesting': self.harvest,
            'logging': self.harvest,
            'mining': self.harvest,
            'traded by merchant': self.parse_merchant,
            'desynthesis': self.desynthesis,
            'recipes using': self.used_recipes,
            'used in quest': self.used_quest,
            'used in levequest': self.used_leve,
            'recipes': self.recipes,

        }

    def parse(self):
        table = self.table
        tc = table.tbody.find_all('tr')
        title = str(tc[0].th.div.text)
        true_key = sanitize_string(title)
        tds = tc[1].find_all('td')
        parse_key = str(title).lower().strip()
        result_table = {}

        if 'venture' in parse_key:
            result = self.parse_merchant(tds)
            if len(result.keys()) > 0:
                # print(title)
                result_table[true_key] = result

        else:
            for key in self.parse_dict:
                if key in parse_key:
                    result = self.parse_dict[key](tds)
                    if len(result.keys()) > 0:
                        # print(title)
                        result_table[true_key] = result

        if len(result_table.keys()) > 0:
            # print(result_table)
            return result_table
