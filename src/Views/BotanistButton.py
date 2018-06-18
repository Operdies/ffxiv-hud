from tkinter import StringVar, Button, Label
from tkinter.ttk import Label, Style


class BotanistButton:
    def __init__(self, master, botanisthelper, et, settings, outliner=None):
        self.outliner = outliner
        self.settings = settings
        self.master = master
        self.previous_text = None
        soon = Style()
        self.soon_style = 'soon.TLabel'
        self.regular_style = 'TLabel'
        soon.configure(self.soon_style, background='#DD5500')
        self.botanisthelper = botanisthelper
        self.text = StringVar()
        self.highlight = settings['highlight'] if 'highlight' in settings else False
        self.botanisthelper.highlight = self.highlight
        self.width = 400
        self.height = 30
        self.label = Label(et.minimal_group)

        self.label.bind('<Button-3>', self.toggle_highlight)
        et.updatees += [self.update]

    def toggle_highlight(self, e):
        self.highlight = not self.highlight
        self.settings['highlight'] = self.highlight
        self.botanisthelper.highlight = self.highlight

    def update(self):
        text = self.botanisthelper.report()
        if text != self.previous_text:
            soon = ' in 00:' in text
            if '00:30' in text and not self.settings['muted']:
                self.botanisthelper.play_alert()
            # color = '#DD5500' if soon and self.highlight else '#000000'
            kwargs = {}
            # kwargs = {'bg': color}
            if self.outliner is not None:
                kwargs['image'] = self.outliner.outline(text, self.width, self.height, center=False)
            else:
                self.text.set(text)

            self.label.config(**kwargs)
            self.label.configure(style=self.soon_style if soon and self.highlight else 'TLabel')

        self.previous_text = text
