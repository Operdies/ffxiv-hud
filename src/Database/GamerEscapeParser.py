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
        # headers = Parser.get_headers(tds[0])
        headers = ['Item', 'Skill', 'Level']
        item_names = []
        skills = []
        levels = []
        table_rows = tds[0].table.tbody.find_all('tr')
        for row in table_rows[1:]:
            title, skill = row.find_all('td', recursive=False)
            item_names += [(sanitize_string(title.a.get('title')), 'href')]
            prof = sanitize_string(skill.div.a.get('title'))
            prof = prof.replace('Category:', '').replace('Recipes', '')
            skills += [prof]
            number_text = sanitize_string(skill.text)
            # print(number_text)
            numbers = re.findall('.*?(\d*)\)', number_text)[0]
            # print(numbers)
            levels += [int(numbers[-4:])]

        return {'Item': item_names, 'Skill': skills, 'Level': levels}
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
    def recipes(tr):
        trs = tr.find_all('tr')
        header = ['amount', sanitize_string(' '.join(list(trs[0].stripped_strings)[-4:]))]
        amounts = []
        mats = []
        items = trs[8:]
        for item in items:
            if str(item.td.get('align')) != 'center':
                break
            amounts += [sanitize_string(item.td.text)]
            mats += [(sanitize_string(item.find('a').get('title')), 'href')]

        return dict(zip(header, [amounts, mats]))

    def __init__(self, table):
        self.table = table
        self.parse_dict = {
            'sold by merchant': self.parse_merchant,
            # 'reduction resulting': self.parse_merchant,
            'venture': self.parse_merchant,
            'harvesting': self.harvest,
            'logging': self.harvest,
            'mining': self.harvest,
            # 'traded by merchant': self.parse_merchant,
            # 'traded to': self.parse_merchant,
            # 'desynthesis': self.desynthesis,
            'recipes using': self.used_recipes,
            # 'used in quest': self.used_quest,
            # 'used in levequest': self.used_leve,

        }

    def parse(self):
        table = self.table
        tc = table.tbody.find_all('tr')
        title = str(tc[0].th.div.text)
        true_key = sanitize_string(title)
        tds = tc[1].find_all('td')
        parse_key = str(title).lower().strip()
        result_table = {}
        # print(parse_key)

        result = None
        if 'venture' in parse_key:
            result = self.parse_merchant(tds)
        elif 'recipes' in parse_key and not 'using' in parse_key:
            result = self.recipes(tc[1])
        else:
            for key in self.parse_dict:
                if key in parse_key:
                    result = self.parse_dict[key](tds)

        if result is not None:
            result_table[true_key] = result

        return result_table
