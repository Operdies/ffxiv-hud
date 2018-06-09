from tkinter import StringVar, Button, Label


class BotanistButton:
    def __init__(self, master, et, settings, outliner=None):
        self.outliner = outliner
        self.settings = settings
        self.master = master
        self.previous_text = None
        self.et = et
        self.text = StringVar()
        self.highlight = settings['highlight'] if 'highlight' in settings else False
        self.et.highlight = self.highlight
        self.label = Label(master,
                           fg='#FFFFFF',
                           bg='#000000',
                           width='300',
                           textvariable=self.text,
                           borderwidth=0)

        self.label.bind('<Button-3>', self.toggle_highlight)
        self.init()

    def toggle_highlight(self, e):
        self.highlight = not self.highlight
        self.settings['highlight'] = self.highlight
        self.et.highlight = self.highlight

    def init(self):
        override = 1 if self.settings['movable'] else 0
        # override = 0
        self.master.overrideredirect(override)
        x, y, _, _ = self.get_pos()
        if not override:
            x -= 8
            y -= 32

        # self.master.geometry("+{}+{}".format(x, y))

    def nudge(self):
        direction = 'up' if self.settings['movable'] else 'down'
        delta_y = 32
        delta_x = 8
        x, y, _, _ = self.get_pos()
        if direction is 'down':
            delta_x, delta_y = -delta_x, -delta_y

        self.master.geometry("+{}+{}".format(x + delta_x, y + delta_y))

    def toggle_lock(self):
        # return
        self.settings['movable'] = not self.settings['movable']
        override = 1 if self.settings['movable'] else 0
        delta_y = 32 if override else -32
        delta_x = 8 if override else -8

        self.nudge()
        self.master.overrideredirect(override)

        print(self.settings['movable'])

    def get_pos(self, ele=None):
        ele = self.master if ele is None else ele
        return ele.winfo_x(), ele.winfo_y(), ele.winfo_height(), ele.winfo_width()

    def update(self):
        text = self.et.report()
        if text != self.previous_text:
            soon = ' in 00:' in text
            color = '#DD5500' if soon and self.highlight else '#000000'
            kwargs = {'bg':color}
            if self.outliner is not None:
                _, _, h, w = self.get_pos(self.label)
                kwargs['image'] = self.outliner.outline(text, w, h)
            else:
                self.text.set(text)

            self.label.config(**kwargs)
        self.previous_text = text
