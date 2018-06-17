from tkinter import *
from tkinter import ttk


class ItemView:
    def __init__(self, master, et, db, frame, wd):
        styles = ttk.Style()
        styles.configure('TopBar.TFrame', background='#202223')
        styles.configure('SearchBar.TEntry', foreground='black')

        self.frame = frame
        self.db = db
        self.wd = wd
        self.et = et
        self.text = StringVar()
        self.master = master
        self.search_bar = self.make_searchfield()
        # frame.rowconfigure(0, weight=0)

    def make_searchfield(self, entry_column=10):
        self.frame.columnconfigure(5, weight=0)
        self.frame.rowconfigure(1, weight=1)
        text = ttk.Entry(self.frame,
                         width=15,
                         textvariable=self.text,
                         style='SearchBar.TEntry')
        text.grid(column=entry_column, row=0, sticky=W)
        text.bind('<Return>', self.onReturn)
        top_bar = ttk.Frame(self.frame, width=100, style='TopBar.TFrame')
        top_bar.grid(column=0, row=0, columnspan=10, sticky=N + S + E + W)
        self.frame.columnconfigure(0, weight=1)
        self.wd(top_bar, self.master)
        self.frame.columnconfigure(10, weight=0)
        self.frame.rowconfigure(0, weight=0)
        return text

    def onReturn(self, e):
        text = self.text.get()  # self.entry.get('0.0', END)
        print(text)
        text = text.replace('\n', '')
        tables = self.db.get_tables(text)
        valid_tables = [table for table in tables if table is not None]
        print(valid_tables)
        print(len(valid_tables))
        # self.text.delete('0.0', 'end')
        self.create_table(valid_tables[0], text)

    def create_table(self, table, item):
        start_column = 5
        start_row = 5
        for child in list(self.frame.winfo_children()):
            child.destroy()
        kwargs = {'fg': 'white', 'bg': '#323435'}
        key = list(table.keys())[0]
        header = key
        t = table[key]
        num_columns = len(t.keys())
        self.search_bar = self.make_searchfield(entry_column=10)

        Label(master=self.frame, text=item.title(), **kwargs).grid(column=start_column, row=start_row - 2,
                                                                   columnspan=len(t.keys()))
        Label(master=self.frame, text=header, **kwargs).grid(column=start_column, row=start_row - 1, columnspan=len(t.keys()))
        # table = ttk.LabelFrame(column = )

        column = start_column
        for key in t:
            row = start_row
            Label(master=self.frame, text=key, **kwargs).grid(column=column, row=row, sticky=W)
            self.frame.columnconfigure(column, weight=1)

            for value in t[key]:
                row += 1
                Label(master=self.frame, text=value, **kwargs).grid(column=column, row=row, sticky=W)
            print(column)
            column += 1