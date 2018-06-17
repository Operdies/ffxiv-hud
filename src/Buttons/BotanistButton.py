from tkinter import StringVar, Button, Label


class BotanistButton:
    def __init__(self, master, botanisthelper, et, settings, outliner=None):
        self.outliner = outliner
        self.settings = settings
        self.master = master
        self.previous_text = None
        self.botanisthelper = botanisthelper
        self.text = StringVar()
        self.highlight = settings['highlight'] if 'highlight' in settings else False
        self.botanisthelper.highlight = self.highlight
        self.label = Label(et.minimal_group,
                           fg='#FFFFFF',
                           bg='#000000',
                           width='280',
                           height=2,
                           textvariable=self.text,
                           borderwidth=0)

        self.label.bind('<Button-3>', self.toggle_highlight)
        et.updatees += [self.update]

    def toggle_highlight(self, e):
        self.highlight = not self.highlight
        self.settings['highlight'] = self.highlight
        self.botanisthelper.highlight = self.highlight

    def get_pos(self, ele=None):
        ele = self.master if ele is None else ele
        return ele.winfo_x(), ele.winfo_y(), ele.winfo_height(), ele.winfo_width()

    def update(self):
        text = self.botanisthelper.report()
        if text != self.previous_text:
            soon = ' in 00:' in text
            color = '#DD5500' if soon and self.highlight else '#000000'
            kwargs = {'bg': color}
            if self.outliner is not None:
                _, _, h, w = self.get_pos(self.label)
                kwargs['image'] = self.outliner.outline(text, w, h)
            else:
                self.text.set(text)

            self.label.config(**kwargs)
        self.previous_text = text
