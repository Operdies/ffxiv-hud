from .Views import VentureButton, MuteButton, BotanistButton, GPButton, Expand, ItemView
from .Database import Crawler
from .Utils import FileDict, Outliner
from .Utils import WindowDraggaable
from tkinter import Button, PhotoImage, Frame, Grid, N, S, E, W, VERTICAL
from tkinter.ttk import Frame, Separator
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
        kwargs = {'sticky': 'nsew'}
        row = 10

        self.botanist_button.label.grid(column=1, row=row, **kwargs, padx=5)
        self.gpbutton.button.grid(column=3, row=row, sticky='nsew')  # , padx=small_pad)
        self.mute_button.grid(column=5, row=row, **kwargs)
        i = 7
        for b in self.ventures:
            b.button.grid(column=i, row=row, **kwargs)  # , padx=small_pad)
            i += 2

        self.expander.button.grid(column=11, row=row, sticky='esn')
        # for i in range(2, 13, 2):
        #     Separator(self.minimal_group, orient=VERTICAL).grid(row=row, column=i, sticky='ns')

        self.minimal_group.grid(column=0, row=1, sticky='sew')
        Grid.columnconfigure(self.master, 0, weight=1)
        self.minimal_group.columnconfigure(4, weight=0)
        Grid.columnconfigure(self.minimal_group, 4, weight=0)
        Grid.columnconfigure(self.minimal_group, 1, weight=1)
        Grid.rowconfigure(self.master, 0, weight=1)
        self.large_view.grid(column=0, row=0, sticky='nsew')
        self.large_view.rowconfigure(0, weight=1)
