from time import time
from tkinter import Label, Menu, StringVar
from tkinter.ttk import Label


class GPButton:
    def __init__(self, master, et, gpregen=6, max_gp=718, outliner=None, reader=None):
        self.reader = reader
        self.text = StringVar()
        self.outliner = outliner
        self.max_gp = max_gp
        self.gp_sec = gpregen / 3#.356
        self.start = time()
        self._gp = 700  # self.max_gp
        self.recent = None
        self.previous_text = None
        self.photo = None
        self.button = Label(et.minimal_group, textvariable=self.text)
        self.height = 30
        self.width = 90

        self.commands = [
            ('set gp >:]', lambda: None),
        ]
        for i in range(0, max_gp, 100):
            self.commands += [(str(i), self.set_gp(i))]
        self.init_context()
        et.updatees += [self.update]

    @property
    def gp(self):
        return self._gp

    @gp.setter
    def gp(self, value):
        if value <= 0:
            self._gp = 0
        elif value >= self.max_gp:
            self._gp = self.max_gp
        else:
            self._gp = value
        self.start = time()

    def init_context(self):
        rmenu = Menu(None, tearoff=0, takefocus=0)

        for text, cmd in self.commands:
            rmenu.add_command(label=text, command=cmd)

        rmenu.entryconfigure(0, state='disabled', activebackground='#DDDDDD')
        self.button.bind("<Button-3>", lambda b: rmenu.tk_popup(b.x_root + 40, b.y_root + 10, entry="0"))
        # self.button.bind('<Button-1>', lambda b: self.use_recent())
        self.button.bind('<MouseWheel>', self.on_scroll)

    def on_scroll(self, event):
        delta = event.delta
        sign = 1 if delta > 0 else -1
        # gp, _ = self.get_gp()
        self.max_gp = self.max_gp + sign# * 10
        # self.start = time()

    def set_gp(self, value):
        def new():
            # self.start = time()
            self.max_gp = value
            # self.recent = new

        return new

    def use_recent(self):
        self.recent() if self.recent is not None else None

    def get_gp(self):
        elapsed = time() - self.start
        current_gp = min(int(self.gp + self.gp_sec * elapsed), self.max_gp)
        missing_gp = self.max_gp - current_gp
        time_remaining = max(int(missing_gp / self.gp_sec), 0)
        return current_gp, time_remaining

    def update(self):
        if self.reader is not None:
            gp = self.reader.get_gp()
            self.gp = gp

        current, remaining = self.get_gp()
        current = self.gp

        if remaining > 0:
            text = '({2}) {0} / {1}'.format(current, self.max_gp, remaining)
        else:
            text = str(self.max_gp)
        if text == self.previous_text:
            return
        self.previous_text = text
        text += ' GP'
        self.text.set(text)

        # fraction = current / self.max_gp
        # self.photo = self.outliner.outline(text, self.width, self.height, bg=(255, 255, 0, 1), bg_fraction=fraction)
        # self.button.config(image=self.photo)
