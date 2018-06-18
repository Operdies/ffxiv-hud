from tkinter import StringVar, Button, Label
from tkinter.ttk import Label, Button


class Expand:
    def __init__(self, master, et, settings, win32_enumhandler):
        self.win32_enumhandler = win32_enumhandler
        self.master = master
        self.big = not settings['movable']
        self.text = StringVar()
        self.et = et
        self.button = Button(et.minimal_group, textvariable=self.text, command=self.toggle_lock)
        self.settings = settings
        # self.update()
        self.et.one_time_updates += [self.update]
        # et.updatees += [self.win32_enumhandler]

    def get_pos(self, ele=None):
        ele = self.master if ele is None else ele
        return ele.winfo_x(), ele.winfo_y(), ele.winfo_height(), ele.winfo_width()

    def set_override(self):
        override = 1 if self.settings['movable'] else 0
        self.master.overrideredirect(override)

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
        self.update()
        self.nudge()
        self.big = not self.big

    def update(self, first=False):
        self.win32_enumhandler()
        self.text.set('^' if self.big else 'v')
        self.set_override()
