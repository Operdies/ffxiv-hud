from time import time
from tkinter import Label, Menu, StringVar


class GPButton:
    def __init__(self, master, et, gpregen=6, max_gp=718, outliner=None):
        self.outliner = outliner
        self.max_gp = max_gp
        self.gp_sec = gpregen / 3#.356
        self.start = time()
        self._gp = 700  # self.max_gp
        self.recent = None
        self.previous_text = None
        self.photo = None
        self.button = Label(et.minimal_group,
                            fg='#FFFFFF',
                            bg='#000000',
                            # width=80 if self.outliner else 10,
                            width=80,
                            #height=12,
                            highlightthickness=0,
                            # command=self.start_timer,
                            # textvariable=self.text,
                            borderwidth=0)

        self.commands = [
            ('set gp >:]', lambda: None),
        ]
        for i in range(0, max_gp, 100):
            self.commands += [(str(i), self.set_gp(i))]
        self.init_context()
        et.updatees += [self.update ]

    @property
    def gp(self):
        return self._gp

    @gp.setter
    def gp(self, value):
        if 0 <= value <= self.max_gp:
            self._gp = value

    def init_context(self):
        rmenu = Menu(None, tearoff=0, takefocus=0)

        for text, cmd in self.commands:
            rmenu.add_command(label=text, command=cmd)

        rmenu.entryconfigure(0, state='disabled', activebackground='#DDDDDD')
        self.button.bind("<Button-3>", lambda b: rmenu.tk_popup(b.x_root + 40, b.y_root + 10, entry="0"))
        self.button.bind('<Button-1>', lambda b: self.use_recent())
        self.button.bind('<MouseWheel>', self.on_scroll)

    def on_scroll(self, event):
        delta = event.delta
        sign = 1 if delta > 0 else -1
        gp, _ = self.get_gp()
        self.gp = gp + sign * 10
        self.start = time()

    def set_gp(self, value):
        def new():
            self.start = time()
            self.gp = value
            self.recent = new

        return new

    def use_recent(self):
        self.recent() if self.recent is not None else None

    def get_pos(self, ele):
        return ele.winfo_x(), ele.winfo_y(), ele.winfo_height(), ele.winfo_width()

    def get_gp(self):
        elapsed = time() - self.start
        current_gp = min(int(self.gp + self.gp_sec * elapsed), self.max_gp)
        missing_gp = self.max_gp - current_gp
        time_remaining = max(int(missing_gp / self.gp_sec), 0)
        return current_gp, time_remaining

    def update(self):
        current, remaining = self.get_gp()
        if remaining > 0:
            text = '{} / {} ({})'.format(current, self.max_gp, remaining)
        else:
            text = str(self.max_gp)
        if text == self.previous_text:
            return
        self.previous_text = text
        # self.text.set(text)

        fraction = current / self.max_gp
        _, _, h, w = self.get_pos(self.button)
        self.photo = self.outliner.outline(text, w, h, bg=(255, 255, 0, 1), bg_fraction=fraction)
        self.button.config(image=self.photo)
