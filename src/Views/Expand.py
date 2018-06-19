from tkinter import StringVar, Button, Label
from tkinter.ttk import Label, Button
from PIL import Image, ImageTk


class Expand:
    def __init__(self, master, et, settings, win32_enumhandler):
        """

        :param master:
        :param et:
        :param settings:
        :param win32_enumhandler:
        """
        self.win32_enumhandler = win32_enumhandler
        self.master = master
        self.borders_icon = ImageTk.PhotoImage(Image.open('icons/retract.png'))
        self.no_borders_icon = ImageTk.PhotoImage(Image.open('icons/expand.png'))
        self.big = settings['movable']
        self.text = StringVar()
        self.et = et
        self.button = Label(et.minimal_group, image=self.get_icon())
        self.button.bind('<Button-1>', self.toggle_lock)
        self.button.bind('<Button-3>', self.resize_toggle)
        self.settings = settings
        self.et.one_time_updates += [self.update]
        # et.updatees += [self.win32_enumhandler]

    def get_icon(self):
        return self.borders_icon if self.big else self.no_borders_icon

    def get_pos(self):
        ele = self.master
        return ele.winfo_x(), ele.winfo_y(), ele.winfo_height(), ele.winfo_width()

    def set_override(self):
        override = 0 if self.settings['movable'] else 1
        self.master.overrideredirect(override)

    def nudge(self):
        """
        set_override toggles window borders, but the window is anchored by its topleft corner
        when the border is removed we therefore need to adjust the window position as to not nudge
        the window slightly when toggling. A more apt name for this function would be prevent-nudge
        """
        direction = 'down' if self.settings['movable'] else 'up'
        delta_y = 32
        delta_x = 8
        x, y, _, _ = self.get_pos()
        if direction is 'down':
            delta_x, delta_y = -delta_x, -delta_y

        self.master.geometry("+{}+{}".format(x + delta_x, y + delta_y))

    def toggle_lock(self, e=None):
        self.settings['movable'] = not self.settings['movable']
        self.big = self.settings['movable']
        self.update()
        self.nudge()

    def resize_toggle(self, e=None):
        if self.big:
            height = 20
        else:
            height = 600

        self.et.set_height(height)
        self.toggle_lock()

    def update(self, first=False):
        self.win32_enumhandler()
        self.et.updatees += [self.win32_enumhandler]
        self.button.configure(image=self.get_icon())
        self.set_override()
