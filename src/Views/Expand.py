from tkinter import StringVar, Button, Label
from tkinter.ttk import Label, Button


class Expand:
    def __init__(self, master, et, settings, win32_enumhandler):
        self.win32_enumhandler = win32_enumhandler
        self.master = master
        self.small = not settings['movable']
        self.text = StringVar()
        self.et = et
        # self.button = Button(et.minimal_group,
        #                      bg='gray',
        #                      command=self.toggle_lock,
        #                      textvariable=self.text,
        #                      )
        self.button = Button(et.minimal_group, textvariable=self.text, command=self.toggle_lock)
        self.settings = settings
        self.update()

        # et.updatees += [self.win32_enumhandler]

    def get_pos(self, ele=None):
        ele = self.master if ele is None else ele
        return ele.winfo_x(), ele.winfo_y(), ele.winfo_height(), ele.winfo_width()

    def nudge(self):
        direction = 'up' if self.settings['movable'] else 'down'
        delta_y = 32
        delta_x = 8
        x, y, _, _ = self.get_pos()
        if direction is 'down':
            delta_x, delta_y = -delta_x, -delta_y

        self.master.geometry("+{}+{}".format(x + delta_x, y + delta_y))

    def toggle_lock(self, e=None):
        self.settings['movable'] = not self.settings['movable']
        override = 1 if self.settings['movable'] else 0
        self.master.overrideredirect(override)
        self.update()
        self.nudge()
        self.small = not self.small

    def update(self, first=False):
        self.win32_enumhandler()
        self.text.set('^' if self.small else 'v')
