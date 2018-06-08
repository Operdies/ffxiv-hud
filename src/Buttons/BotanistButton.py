from tkinter import StringVar, Button, Label


class BotanistButton:
    def __init__(self, master, et, settings):
        self.settings = settings
        self.master = master
        self.et = et
        self.text = StringVar()
        self.highlight = settings['highlight'] if 'highlight' in settings else False
        self.et.highlight = self.highlight
        self.button = Label(master, height=2,
                            fg='#FFFFFF',
                            bg='#000000',
                            #justify='left',
                            #anchor='n',
                            #width=100,
                            highlightthickness=0,
                            highlightcolor="#37d3ff",
                            highlightbackground="#37d3ff",
                            # font='bold',
                            # command=self.toggle_lock,
                            textvariable=self.text,
                            borderwidth=2)

        self.button.bind('<Button-3>', self.toggle_highlight)
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

    def get_pos(self):
        ele = self.master
        return ele.winfo_x(), ele.winfo_y(), ele.winfo_height(), ele.winfo_width()

    def update(self):
        text, cb = self.et.report()
        cb()
        soon = ' in 00:' in text
        color = '#DD5500' if soon and self.highlight else '#000000'
        self.button.config(bg=color, width=int(len(text)*0.6))
        self.text.set(text)
