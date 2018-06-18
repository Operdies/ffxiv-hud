from tkinter import *
from tkinter import ttk
<< << << < HEAD
from tkinter.ttk import Label, Notebook, Frame, Separator
== == == =
from tkinter.ttk import Label, Notebook, Frame
>> >> >> > 44334
c116c3d3c9df58c1aa1ec927a32ce923a64
import threading


def run_in_thread(fn):
    def run(*k, **kw):
        t = threading.Thread(target=fn, args=k, kwargs=kw)
        t.start()
        return t  # <-- this is new!

    return run


class ItemView:
    def __init__(self, master, et, db, frame, wd):
        # styles = ttk.Style()
        # styles.configure('TopBar.TFrame', background='#202223')
        # styles.configure('SearchBar.TEntry', foreground='black')

        self.frame = frame
        self.db = db
        self.wd = wd
        self.et = et
        self.text = StringVar()
        self.text.set('Search GamerEscape here')
        self.master = master
        self.search_bar = self.make_searchfield()
        self.et.one_time_updates += [lambda: self.get_tables('lightning shard')]
        # frame.rowconfigure(0, weight=0)

    def make_searchfield(self, entry_column=10):
        self.frame.columnconfigure(5, weight=0)
        self.frame.rowconfigure(1, weight=1)
        text = ttk.Entry(self.frame,
                         width=50,
                         textvariable=self.text)
        text.grid(column=entry_column, row=0, sticky=W, padx=5, pady=5)
        text.bind('<Return>', self.on_return)
        text.bind('<Button-1>', self.on_click)
        top_bar = ttk.Frame(self.frame, width=100)
        top_bar.grid(column=0, row=0, columnspan=10, sticky=N + S + E + W)
        self.frame.columnconfigure(0, weight=1)
        self.wd(top_bar, self.master)
        self.frame.columnconfigure(10, weight=0)
        self.frame.rowconfigure(0, weight=0)

        return text

    def on_return(self, e):
        text = self.text.get()  # self.entry.get('0.0', END)
        print(text)
        text = text.replace('\n', '')
        print('working on it...')
        self.text.set('searching for {}...'.format(self.text.get()))

        self.get_tables(text)

    def on_click(self, e):
        self.search_bar.select_clear()
        self.search_bar.select_range(0, 'end')
        self.search_bar.focus()
        return 'break'

    @run_in_thread
    def get_tables(self, text):
        tables, ret_code = self.db.get_tables(text)

        def callback():
            if ret_code == 200:
                self.create_table(tables, text)
                self.text.set('showing results for {}'.format(text))
            else:
                self.text.set('Something bad happend ({})'.format(ret_code))

        self.et.one_time_updates += [callback]

    def create_table(self, tables, item):
        for child in list(self.frame.winfo_children()):
            child.destroy()

        self.search_bar = self.make_searchfield(entry_column=10)
        nb = Notebook(self.frame)
        nb.grid(column=0, row=1, columnspan=15, sticky='nsew')
        self.frame.columnconfigure(0, weight=1)

        for t in tables:
            table_key = list(t)[0]
            t = t[table_key]
            table_frame = Frame(nb)
            nb.add(table_frame, text=table_key)
            self.create_column(t, table_frame)

    def create_column(self, table, table_frame):
        kwargs = {'style': 'table.TLabel'}
        headerkwargs = {'style': 'header.TLabel'}

        column = 1
        row = 1
        for key in table:
            if 'venture' in key.lower():
                name = ' '.join(key.split(' ')[2:4])
            else:
                name = key
            row = 1
            Label(table_frame, text=name, **headerkwargs).grid(column=column, row=row, sticky='n')
            table_frame.columnconfigure(column, weight=1)

            for value in table[key]:
                row += 2
                Label(table_frame, text=value, **kwargs).grid(column=column, row=row)

            column += 2

        padding = 2
        for i in range(2, row + padding, 2):
            Separator(table_frame, orient=HORIZONTAL).grid(row=i, column=0, columnspan=column + 1, sticky='ew')

        for j in range(2, column + padding, 2):
            Separator(table_frame, orient=VERTICAL).grid(row=0, column=j, rowspan=row + 1, sticky='ns')
