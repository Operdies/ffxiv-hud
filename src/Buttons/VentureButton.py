from tkinter import Button, StringVar, Menu
from datetime import timedelta
from time import time
import pickle


class VentureButton:
    def __init__(self, master, fd, name, bg='#000000', venture_length=1):
        self.fd = fd
        self.master = master
        self.name = name
        self.text = StringVar()
        self.text.set(name)
        self.time = timedelta(hours=venture_length)
        self.button = Button(master, height=2,
                             fg='#FFFFFF',
                             bg=bg,
                             width=12,
                             # bd = 2,
                             highlightthickness=0,
                             highlightcolor="#37d3ff",
                             highlightbackground="#37d3ff",
                             command=self.start_timer,
                             textvariable=self.text,
                             borderwidth=0)

        self.commands = [
            (name + ':', lambda: None),
            (" Reset Timer", lambda: self.cancel_venture(None))
        ]
        self.venture_start = fd[name]
        self.venture_active = not self.venture_done()[0]

        self.init_context()
        self.button_config()

    def save_start(self):
        self.fd[self.name] = self.venture_start

    def init_context(self):
        rmenu = Menu(None, tearoff=0, takefocus=0)

        for text, cmd in self.commands:
            rmenu.add_command(label=text, command=cmd)

        rmenu.entryconfigure(0, state='disabled', activebackground='#DDDDDD')
        self.button.bind("<Button-3>", lambda b: rmenu.tk_popup(b.x_root + 40, b.y_root + 10, entry="0"))

    def start_timer(self):
        if not self.venture_active:
            self.venture_start = time()

            self.venture_active = True
            self.save_start()
            # self.button.config(state="disabled")

    def cancel_venture(self, e):
        self.venture_active = False
        self.button_config()

    def button_config(self, text=None):
        red = "#FF0000"
        green = "#00FF00"
        ready = not self.venture_active
        # color = red if not ready else green
        color = '#FFFFFF'
        text = text if not ready else self.name
        #        state = "normal" if ready else "disabled"
        state = "normal" if ready else "normal"
        self.button.config(fg=color, state=state)
        self.text.set(text)

    def venture_done(self):
        elapsed = time() - self.venture_start
        remaining = self.time - timedelta(seconds=elapsed)
        done = remaining < timedelta(0)

        return done, remaining

    def update(self):
        if not self.venture_active:
            return
        done, remaining = self.venture_done()
        if done:
            self.venture_active = False

        text = str(remaining).split('.')[0]
        text = '  ' + text + '  '
        self.button_config(text)
