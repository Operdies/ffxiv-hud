from .Buttons import VentureButton, MuteButton, BotanistButton, GPButton, Expand, ItemView
from .Database import Crawler
from .Utils import FileDict, Outliner
from .Utils import WindowDraggaable
from tkinter import Button, PhotoImage, Frame, Grid, N, S, E, W
from PIL import Image, ImageTk
import re
from time import sleep


class MainWindow:

    def __init__(self, master, botanist_helper, crawler, win32_enumhandler):
        self.master = master
        self.botanist_helper = botanist_helper
        self.minimal_group = Frame(master, bg='black', width=800, height=40)
        self.large_view = Frame(master, bg='#323435')  # , width=800, height='600')

        # self.w = Label(root, textvariable=self.text).pack(side='left')
        master.title('Eorzea Timers')
        venture_dict = FileDict('settings/venture', default=0)
        self.venture_dict = venture_dict
        self.updatees = []  # list of update functions to run
        # other buttons add their own update functions to this

        josuke = VentureButton(master, self, venture_dict, 'Josuke', Outliner(), bg='#4400BB')  # Purple
        haurchefant = VentureButton(master, self, venture_dict, 'Haurchefant', Outliner(), bg='#0077EE')  # Teal

        self.ventures = [josuke, haurchefant]
        self.mute_button = MuteButton(master, self, botanist_helper,
                                      FileDict('settings/mute_state', default=False)).mute_button
        settings_fd = FileDict('settings/settings')
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

        # self.dragger = WindowDraggaable(self.botanist_button.label, master)
        self.pack_buttons()
        # self.mute_button.pack_forget()
        self.toggle_large(True)
        self.itemview = ItemView(master, self, Crawler(), self.large_view, WindowDraggaable)

    def update_loop(self):
        for update in self.updatees:
            update()

    def pack_buttons(self):
        # kwargs = {'expand': True, 'fill': 'both'}
        # self.lock.pack(side='right', fill='both')
        # self.expander.button.pack(side='right', **kwargs)
        # self.gpbutton.button.pack(side='right', **kwargs)
        # for b in self.ventures:
        #     b.button.pack(side='right', fill='y')  # , **kwargs)
        # self.mute_button.pack(side='right', fill='both', expand=True)  # , **kwargs)
        # self.botanist_button.label.pack(side='right', **kwargs)
        # self.minimal_group.pack(expand=False, fill='both', side='bottom')
        kwargs = {'sticky': N + S + E + W,
                  }
        small_pad = 0
        self.expander.button.grid(column=80, row=10, sticky=E + S + N)
        self.gpbutton.button.grid(column=2, row=10, sticky=W + N + S + E)  # , padx=small_pad)
        i = 5
        for b in self.ventures:
            b.button.grid(column=i, row=10, **kwargs)  # , padx=small_pad)
            i += 1
        self.mute_button.grid(column=4, row=10, **kwargs)
        self.botanist_button.label.grid(column=1, row=10, **kwargs, padx=5)
        # self.minimal_group.grid(column=0, row=1, sticky=N+S+E+W)
        self.minimal_group.grid(column=0, row=1, sticky=S + E + W)

        # Grid.rowconfigure(self.master, 0, weight=1)
        Grid.columnconfigure(self.master, 0, weight=1)
        self.minimal_group.columnconfigure(4, weight=1)
        Grid.columnconfigure(self.minimal_group, 1, weight=1)
        Grid.rowconfigure(self.master, 0, weight=1)
        # Grid.rowconfigure(self.minimal_group, 1, weight=1)

    def get_pos(self, ele):
        return ele.winfo_x(), ele.winfo_y(), ele.winfo_height(), ele.winfo_width()

    def toggle_large(self, visible):
        x, y, h, w = self.get_pos(self.master)
        print('\n\n\n')
        print(w, h, x, y)
        if visible:
            h = 600
            w = 800
            print('expanding')
            # x -= 8
            # y -= 32
            # new_h = 600
            # new_y = y - (new_h - h)
            # y = max(100, new_y)
            # y = min(1000, y)
            # h = new_h
            # self.large_view.pack(expand=True, fill='both', side='top')
            self.large_view.grid(column=0, row=0, sticky=N + S + E + W)
            self.large_view.rowconfigure(0, weight=1)
        else:
            h = 100
            print('deflating')
            # x += 8
            # y += 32
            # new_h = 28
            # new_y = y - (new_h - h)
            # y = max(100, new_y)
            # y = min(1000, y)
            # h = new_h
            self.large_view.grid_forget()
        self.master.geometry('{}x{}+{}+{}'.format(w, h, x, y))
