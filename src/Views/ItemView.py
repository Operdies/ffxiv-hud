from tkinter import Text, StringVar, HORIZONTAL, VERTICAL#, Button
from tkinter import ttk, Button
from tkinter.ttk import Label, Notebook, Frame, Separator
from .Tooltip import CreateToolTip
from PIL import ImageTk, Image
import threading


def run_in_thread(fn):
    def run(*k, **kw):
        t = threading.Thread(target=fn, args=k, kwargs=kw)
        t.start()
        return t  # <-- this is new!

    return run


class ItemView:
    def __init__(self, master, et, db, frame, wd):
        self.entry_focused = False
        self.frame = frame
        self.db = db
        self.wd = wd
        self.et = et
        self.left_img = ImageTk.PhotoImage(Image.open('icons/left.png'))
        self.right_img = ImageTk.PhotoImage(Image.open('icons/right.png'))
        self.nb = None
        self.text = StringVar()
        self.previous_searches = []
        self.future_searches = []
        self.current_search = None
        self.search_loc = 0
        self.text.set('Search GamerEscape here')
        self.master = master
        self.search_bar = self.make_searchfield()
        # self.et.one_time_updates += [lambda: self.execute_search('hingan flax', from_entry=True)]
        # self.et.one_time_updates += [lambda: self.execute_search('flax', from_entry=True)]
        # self.et.one_time_updates += [lambda: self.execute_search('leather', from_entry=True)]
        self.et.updatees += [self.check_focus]

    def make_searchfield(self, entry_column=9):
        darker_grey = '#272627'
        self.frame.columnconfigure(5, weight=0)
        self.frame.rowconfigure(1, weight=1)
        master_frame = Frame(self.frame)
        master_frame.grid(column=0, row=0, sticky='nsew')
        master_frame.columnconfigure(0, weight=1)
        master_frame.rowconfigure(1, weight=1)
        text = ttk.Entry(master_frame,
                         width=50,
                         textvariable=self.text)
        text.grid(column=entry_column, row=0, sticky='w', padx=5, pady=5)
        text.bind('<Return>', self.on_return)
        text.bind('<Button-1>', self.on_click)

        left_button = Button(master_frame, bg=darker_grey, image=self.left_img, relief='flat',
                             command=lambda: self.traverse_searches(-1))
        right_button = Button(master_frame, bg=darker_grey, image=self.right_img, relief='flat',
                              command=lambda: self.traverse_searches(1))
        left_button.grid(column=entry_column - 2, row=0, padx=(0, 15))
        right_button.grid(column=entry_column - 1, row=0)
        # left_button.bind('<Button-1>', lambda e: self.traverse_searches(-1))
        # right_button.bind('<Button-1>', lambda e: self.traverse_searches(1))
        self.left_button = left_button
        self.right_button = right_button

        top_bar = ttk.Frame(master_frame)  # , width=100)
        top_bar.grid(column=0, row=0, sticky='nsew')
        self.frame.columnconfigure(0, weight=1)
        self.wd(top_bar, self.master, self.et)
        self.frame.rowconfigure(0, weight=0)
        self.update_buttons()


        return text

    def on_return(self, e):
        text = self.text.get()  # self.entry.get('0.0', END)
        text = text.replace('\n', '')
        self.execute_search(text, from_entry=True)

    def execute_search(self, text, from_entry=False):
        if from_entry:
            if self.current_search is not None:
                self.previous_searches += [self.current_search]
                self.future_searches = []

            self.current_search = text

        self.text.set('searching for {}...'.format(text))
        print('working on it...')
        self.get_tables(text)

    def traverse_searches(self, direction):
        print(self.previous_searches)
        print(self.future_searches)
        if direction > 0:
            search = self.future_searches.pop()
            self.previous_searches += [self.current_search]
        else:
            search = self.previous_searches.pop()
            self.future_searches += [self.current_search]

        self.execute_search(search)
        self.current_search = search
        print(self.previous_searches)
        print(self.future_searches)

    def on_click(self, e):
        self.search_bar.select_clear()
        self.search_bar.select_range(0, 'end')
        self.search_bar.focus()
        self.entry_focused = True
        return 'break'

    def check_focus(self):
        focus = str(self.search_bar.focus_get())
        self.entry_focused = 'entry' in focus.lower()

    def update_buttons(self):
        self.left_button.configure(state='normal' if self.previous_searches else 'disabled')
        self.right_button.configure(state='normal' if self.future_searches else 'disabled')
        self.update_button_tooltips()

    def update_button_tooltips(self):
        if self.previous_searches:
            CreateToolTip(self.left_button, self.previous_searches[-1])
        if self.future_searches:
            CreateToolTip(self.right_button, self.future_searches[-1])

    @run_in_thread
    def get_tables(self, text):
        tables, ret_code = self.db.get_tables(text)

        def callback():
            if ret_code == 200:
                self.create_table(tables, text)
                self.text.set('showing results for {}'.format(text))
                self.update_buttons()
            else:
                self.text.set('Something bad happend ({})'.format(ret_code))

        self.et.one_time_updates += [callback]

    def create_table(self, tables, item):
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

        nb.bind('<MouseWheel>', self.on_scroll)

    def on_scroll(self, event):
        delta = event.delta
        sign = -1 if delta > 0 else 1
        new = self.nb.index('current') + sign
        new = max(0, new)
        new = min(new, len(self.nb.tabs()) - 1)
        self.nb.select(new)

    def get_func(self, value):
        def cb(e):
            self.execute_search(value, from_entry=True)

        return cb

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
            Label(table_frame, text=name, **headerkwargs).grid(column=column, row=row, sticky='n', padx=1, pady=1)
            table_frame.columnconfigure(column, weight=1)

            for value in table[key]:
                row += 2
                addon = None
                if hasattr(value, '__iter__') and type(value) is not str:
                    value, addon = value
                # value = ItemView.wrap_text(value)
                label = Label(table_frame, text=value, **kwargs, wraplength=200)
                label.grid(column=column, row=row, sticky='w', padx=5, pady=0)
                if addon == 'href':
                    label.configure(style='href.TLabel')
                    label.bind('<Button-1>', self.get_func(value))
                    # print('href', value)

            column += 2

        padding = 2
        for i in range(2, row + padding, 2):
            Separator(table_frame, orient=HORIZONTAL).grid(row=i, column=0, columnspan=column + 1, sticky='ew')

        for j in range(2, column, 2):
            Separator(table_frame, orient=VERTICAL).grid(row=0, column=j, rowspan=row + 1, sticky='ns')

    @staticmethod
    def wrap_text(text, maxlength=32):
        lines = []
        for line in text.split('\n'):
            if len(line) <= maxlength:
                lines += [line]
                continue

            half = int(len(line) / 2)
            split_place = None
            for i in range(0, half):
                if line[half + i] == ' ':
                    split_place = half + i
                    break
                elif line[half - i] == ' ':
                    split_place = half - i
                    break
            print('breaking text at {} of {}'.format(split_place, len(line)))

            if split_place is not None:
                line = line[:split_place] + '\n' + line[split_place + 1:]
                lines += [line]
            else:
                lines += [line]

        return '\n'.join(lines)
