from tkinter import ttk, font


def apply_styles():
    table_width = 30
    dark_grey = '#313031'
    darker_grey = '#272627'
    styles = ttk.Style()
    styles.configure('.', background=darker_grey, font=('helvetica', 9))
    styles.configure('TFrame', background=darker_grey, padx=10)
    styles.configure('alt.TFrame', background=dark_grey)
    styles.configure('TEntry', foreground='black')
    styles.configure('TLabel', background=darker_grey, foreground='white', anchor='center')
    styles.configure('header.TLabel',
                     foreground='white',
                     anchor='center',
                     # width=table_width,
                     bd=1,
                     highlightbackground='white')
    styles.configure('TButton')
    styles.configure('table.TLabel', background=darker_grey,
                     justify='w',
                     bd=1,
                     anchor='center',
                     foreground="white",
                     highlightbackground='white')
    styles.configure('href.TLabel', background=darker_grey,
                     justify='w',
                     bd=1,
                     anchor='center',
                     foreground="white",
                     highlightbackground='white',
                     font=('helvetica', 9, 'underline')
                     )

    styles.configure('TNotebook', background=darker_grey, bd=1, highlightbackground='red', highlightcolor='red')
