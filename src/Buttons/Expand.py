from tkinter import StringVar, Button, Label


class Expand:
    def __init__(self, master, et, settings, win32_enumhandler):
        self.win32_enumhandler = win32_enumhandler
        self.master = master
        self.small = not settings['movable']
        self.text = StringVar()
        self.et = et
        self.button = Button(et.minimal_group,
                             bg='gray',
                             command=self.toggle_lock,
                             textvariable=self.text,
                             )
        self.settings = settings
        # self.init()
        self.toggle_lock()
        self.toggle_lock()

        # et.updatees += [self.win32_enumhandler]

    def init(self):
        override = 1 if self.settings['movable'] else 0
        # override = 0
        self.master.overrideredirect(override)
        x, y, _, _ = self.get_pos()
        self.update(first=True)

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

    def toggle_lock(self):
        self.settings['movable'] = not self.settings['movable']
        override = 1 if self.settings['movable'] else 0
        self.master.overrideredirect(override)
        self.update()
        self.nudge()
        self.small = not self.small
        # if not self.small:
        #     self.master.call('wm', 'attributes', '.', '-topmost', '1')
        # else:
        #     self.master.call('wm', 'attributes', '.', '-topmost', '0')

    def update(self, first=False):
        self.win32_enumhandler()
        self.text.set('^' if self.small else 'v')
        # if not first:
        #     self.et.toggle_large(visible=not self.small)
