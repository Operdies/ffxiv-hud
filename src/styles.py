from tkinter import ttk


def apply_styles():
    dark_grey = '#313031'
    darker_grey = '#272627'
    styles = ttk.Style()
    styles.configure('TFrame', background=darker_grey, padx=10)
    styles.configure('alt.TFrame', background=dark_grey)
    styles.configure('TEntry', foreground='black')
    styles.configure('TLabel', background=darker_grey)
    styles.configure('TButton')
