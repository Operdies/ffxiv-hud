from tkinter import Frame
from .Buttons import VentureButton, MuteButton, BotanistButton
from .Utils import FileDict
from .Utils import WindowDraggaable


class MainWindow:

    def __init__(self, master, et):
        self.master = master
        self.et = et

        # self.w = Label(root, textvariable=self.text).pack(side='left')
        master.title('Eorzea Timers')
        # frame = Frame(master,
        #              highlightthickness=1,
        #              bd=10,
        #              takefocus=0,
        #              width=80,
        #              highlightcolor="#000000",
        #              highlightbackground="#000000",)
        # frame.pack(expand=True, fill='both', side='top')
        # frame.config(bg='#000000')
        venture_dict = FileDict('venture', default=0)
        self.venture_dict = venture_dict

        haurchefant = VentureButton(master, venture_dict, 'Haurchefant', bg='#0077EE')  # Teal
        josuke = VentureButton(master, venture_dict, 'Josuke', bg='#4400BB')  # Purple

        self.ventures = [josuke, haurchefant]
        self.mute_button = MuteButton(master, et).mute_button
        self.botanist_button = BotanistButton(master, et, FileDict('settings'))
        WindowDraggaable(self.botanist_button.button, master)
        self.updates = [v.update for v in self.ventures] + [self.botanist_button.update]

        self.pack_buttons()
        # self.mute_button.pack_forget()

    def update_loop(self):
        for update in self.updates:
            update()

    def pack_buttons(self):
        kwargs = {'expand': True, 'fill': 'both'}

        self.botanist_button.button.pack(side='left', **kwargs)
        for b in self.ventures:
            b.button.pack(side='right', fill='y')  # , **kwargs)
        self.mute_button.pack(side='right', fill='y')  # , **kwargs)
