from tkinter import *
from tkinter import ttk
from tkinter.ttk import Label, Notebook, Frame
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
        nb.grid(column=0, row=1, columnspan=15, sticky='nw')
        self.frame.columnconfigure(0, weight=1)

        for t in tables:
            table_key = list(t.keys())[0]
            t = t[table_key]
            kwargs = {'style': 'table.TLabel'}
            headerkwargs = {'style': 'header.TLabel'}
            table_frame = Frame(nb)
            nb.add(table_frame, text=table_key)

            column = 0
            for key in t:
                if 'venture' in key.lower():
                    name = ' '.join(key.split(' ')[2:4])
                else:
                    name = key
                row = 0
                Label(table_frame, text=name, **headerkwargs).grid(column=column, row=row, sticky='n')
                table_frame.columnconfigure(column, weight=1)

                for value in t[key]:
                    row += 1
                    Label(table_frame, text=value, **kwargs).grid(column=column, row=row)
                # print(column)
                column += 1
