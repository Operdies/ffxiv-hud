from tkinter import Button, StringVar, Menu, Label
from datetime import timedelta
from time import time
import pickle


class VentureButton:
    def __init__(self, master, fd, name, outliner, bg='#000000', venture_length=1):
        self.outliner = outliner
        self.fd = fd
        self.bg = bg
        self.master = master
        self.name = name
        self.text = StringVar()
        self.previous_text = None
        self.text.set(name)
        self.time = timedelta(hours=venture_length)
        self.button = Label(master,
                            fg='#FFFFFF',
                            bg=bg,
                            width=80 if self.outliner else 10,
                            highlightthickness=0,
                            # command=self.start_timer,
                            textvariable=self.text,
                            borderwidth=0)

        self.commands = [
            (name + ':', lambda: None),
            (" Reset Timer", lambda: self.cancel_venture(None))
        ]
        self.venture_start = fd[name]
        self.venture_active = not self.venture_done()[0]

        self.init_context()
        self.button_config(*self.venture_done())

    def save_start(self):
        self.fd[self.name] = self.venture_start

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

            self.venture_active = True
            self.save_start()
            # self.button.config(state="disabled")

    def cancel_venture(self, e):
        self.button_config(done=True, remaining=None)

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
        if not self.venture_active:
            return
        self.button_config(*self.venture_done())
