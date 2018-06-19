from tkinter import Text, StringVar, HORIZONTAL, VERTICAL
from tkinter import ttk
from tkinter.ttk import Label, Notebook, Frame, Separator
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
        self.entry_focused = False
        self.frame = frame
        self.db = db
        self.wd = wd
        self.et = et
        self.nb = None
        self.text = StringVar()
        self.text.set('Search GamerEscape here')
        self.master = master
        self.search_bar = self.make_searchfield()
        self.et.one_time_updates += [lambda: self.get_tables('hingan flax')]
        self.et.updatees += [self.check_focus]

    def make_searchfield(self, entry_column=10):
        self.frame.columnconfigure(5, weight=0)
        self.frame.rowconfigure(1, weight=1)
        text = ttk.Entry(self.frame,
                         width=50,
                         textvariable=self.text)
        text.grid(column=entry_column, row=0, sticky='w', padx=5, pady=5)
        text.bind('<Return>', self.on_return)
        text.bind('<Button-1>', self.on_click)
        top_bar = ttk.Frame(self.frame, width=100)
        top_bar.grid(column=0, row=0, columnspan=10, sticky='nsew')
        self.frame.columnconfigure(0, weight=1)
        self.wd(top_bar, self.master, self.et)
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
        self.entry_focused = True
        return 'break'

    def check_focus(self):
        focus = str(self.search_bar.focus_get())
        self.entry_focused = 'entry' in focus.lower()

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
        # for child in list(self.frame.winfo_children()):
        #     child.destroy()
        #
        # self.search_bar = self.make_searchfield(entry_column=10)
        if self.nb is not None:
            self.nb.destroy()
        nb = Notebook(self.frame)
        self.nb = nb
        nb.grid(column=0, row=1, columnspan=15, sticky='ne', padx=10, pady=10)
        self.frame.columnconfigure(0, weight=1)

        for t in tables:
            table_key = list(t)[0]
            t = t[table_key]
            table_frame = Frame(nb)
            nb.add(table_frame, text=table_key, sticky='nsew')
            self.create_column(t, table_frame)

    @staticmethod
    def create_column(table, table_frame):
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
            Label(table_frame, text=name, **headerkwargs).grid(column=column, row=row, sticky='n', padx=1, pady=1)
            table_frame.columnconfigure(column, weight=1)

            for value in table[key]:
                row += 2
                Label(table_frame, text=value, **kwargs).grid(column=column, row=row, sticky='w', padx=1, pady=1)

            column += 2

        padding = 2
        for i in range(2, row + padding, 2):
            Separator(table_frame, orient=HORIZONTAL).grid(row=i, column=0, columnspan=column + 1, sticky='ew')

        for j in range(2, column, 2):
            Separator(table_frame, orient=VERTICAL).grid(row=0, column=j, rowspan=row + 1, sticky='ns')
