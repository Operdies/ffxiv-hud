from tkinter import Button, StringVar, Menu, Label
from datetime import timedelta
from time import time, sleep
import pickle


class VentureButton:
    def __init__(self, master, et, fd, name, outliner, bg='#000000'):
        self.outliner = outliner
        self.fd = fd
        self.bg = bg
        self.venture_entry = name + '_venture_length'
        self.duration = timedelta(hours=fd[self.venture_entry])
        self.master = master
        self.name = name
        self.text = StringVar()
        self.previous_text = None
        self.text.set(name)
        self.time = timedelta(hours=fd[self.venture_entry])
        self.button = Label(et.minimal_group,
                            fg='#FFFFFF',
                            bg=bg,
                            width=80 if self.outliner else 12,
                            highlightthickness=0,
                            # command=self.start_timer,
                            # textvariable=self.text,
                            borderwidth=0)

        self.commands = [
            (name + ':', lambda: None),
            (" Reset Timer", lambda: self.cancel_venture(None)),
            (" 1 hour venture", self.set_duration(1)),
            ("18 hour venture", self.set_duration(18))
        ]
        self.venture_start = fd[name]
        self.venture_active = not self.venture_done()[0]

        self.init_context()
        et.updatees += [self.update]

    def save_start(self, reset=False):
        self.fd[self.name] = 0 if reset else self.venture_start

    def set_duration(self, value):
        def new():
            self.duration = timedelta(hours=value)
            self.fd[self.venture_entry] = value

        return new

    def init_context(self):
        rmenu = Menu(None, tearoff=0, takefocus=0)

        for text, cmd in self.commands:
            rmenu.add_command(label=text, command=cmd)

        rmenu.entryconfigure(0, state='disabled', activebackground='#DDDDDD')
        self.button.bind("<Button-3>", lambda b: rmenu.tk_popup(b.x_root + 40, b.y_root + 10, entry="0"))
        self.button.bind('<Button-1>', self.start_timer)

    def start_timer(self, e=None):
        if not self.venture_active:
            self.venture_start = time()
            self.time = self.duration
            self.venture_active = True
            self.save_start()
            # self.button.config(state="disabled")

    def cancel_venture(self, e):
        self.time = timedelta(0)
        self.save_start(reset=True)

    def button_config(self, done, remaining):
        if done:
            self.venture_active = False
        color = self.bg if done else 'black'
        text = self.name if done else str(remaining).split('.')[0]
        if self.previous_text == text:
            # if done == True:
            #    self.button.config(bg=)
            return
        # print('Updating text for {}'.format(self.name))

        kwargs = {'bg': color}
        if self.outliner is not None:
            _, _, h, w = self.get_pos(self.button)
            kwargs['image'] = self.outliner.outline(text, w, h)
        else:
            self.text.set('  ' + text + '  ')

        self.previous_text = text
        self.button.config(**kwargs)

    def venture_done(self):
        elapsed = time() - self.venture_start
        remaining = self.time - timedelta(seconds=elapsed)
        done = remaining < timedelta(0)

        return done, remaining

    def get_pos(self, ele=None):
        ele = self.master if ele is None else ele
        return ele.winfo_x(), ele.winfo_y(), ele.winfo_height(), ele.winfo_width()

    def update(self):
        self.button_config(*self.venture_done())
