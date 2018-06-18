from .Views import VentureButton, MuteButton, BotanistButton, GPButton, Expand, ItemView
from .Database import Crawler
from .Utils import FileDict, Outliner
from .Utils import WindowDraggaable
from tkinter import Button, PhotoImage, Frame, Grid, N, S, E, W
from tkinter.ttk import Frame
from PIL import Image, ImageTk
import re
from time import sleep


class MainWindow:

    def __init__(self, master, botanist_helper, crawler, win32_enumhandler):
        self.master = master
        self.botanist_helper = botanist_helper
        self.minimal_group = Frame(master)  # , width=800, height=40)
        self.large_view = Frame(master, style='alt.TFrame')  # , width=800, height='600')
        master.title('Eorzea Timers')
        venture_dict = FileDict('settings/venture', default=0)
        self.venture_dict = venture_dict
        self.updatees = []  # list of update functions to run
        self.one_time_updates = []  # updates that should only run once
        # other buttons add their own update functions to these
        settings_fd = FileDict('settings/settings', default=False)

        josuke = VentureButton(master, self, venture_dict, 'Josuke', Outliner(), bg='#4400BB')  # Purple
        haurchefant = VentureButton(master, self, venture_dict, 'Haurchefant', Outliner(), bg='#0077EE')  # Teal

        self.ventures = [josuke, haurchefant]
        self.mute_button = MuteButton(master, self, botanist_helper, settings_fd).mute_button
        self.settings_fd = settings_fd
        self.botanist_button = BotanistButton(master, botanist_helper, self, settings_fd,
                                              outliner=Outliner())
        self.gpbutton = GPButton(master, self, outliner=Outliner())
        self.expander = Expand(master, self, settings_fd, win32_enumhandler)
        self.lock_image = ImageTk.PhotoImage(Image.open('icons/unlocked.png'))
        self.lock = Button(master,
                           image=self.lock_image,
                           bg='#000000',
                           borderwidth=0,
                           highlightcolor='#000000')

        self.pack_buttons()
        self.itemview = ItemView(master, self, Crawler(), self.large_view, WindowDraggaable)

    def update_loop(self):
        for update in self.updatees:
            update()

        while self.one_time_updates:
            func = self.one_time_updates.pop()
            func()

    def pack_buttons(self):
        kwargs = {'sticky': N + S + E + W}
        self.expander.button.grid(column=80, row=10, sticky=E + S + N)
        self.gpbutton.button.grid(column=2, row=10, sticky=W + N + S + E)  # , padx=small_pad)
        i = 5
        for b in self.ventures:
            b.button.grid(column=i, row=10, **kwargs)  # , padx=small_pad)
            i += 1
        self.mute_button.grid(column=4, row=10, **kwargs)
        self.botanist_button.label.grid(column=1, row=10, **kwargs, padx=5)
        self.minimal_group.grid(column=0, row=1, sticky=S + E + W)

        Grid.columnconfigure(self.master, 0, weight=1)
        self.minimal_group.columnconfigure(4, weight=0)

        Grid.columnconfigure(self.minimal_group, 4, weight=0)
        Grid.columnconfigure(self.minimal_group, 1, weight=1)
        Grid.rowconfigure(self.master, 0, weight=1)

        self.large_view.grid(column=0, row=0, sticky='nsew')
        self.large_view.rowconfigure(0, weight=1)
