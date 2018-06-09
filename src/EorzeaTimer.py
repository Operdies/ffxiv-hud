from .Buttons import VentureButton, MuteButton, BotanistButton
from .Utils import FileDict, Outliner
from .Utils import WindowDraggaable
from tkinter import Button, PhotoImage
from PIL import Image, ImageTk


class MainWindow:

    def __init__(self, master, et):
        self.master = master
        self.et = et

        # self.w = Label(root, textvariable=self.text).pack(side='left')
        master.title('Eorzea Timers')
        venture_dict = FileDict('settings/venture', default=0)
        self.venture_dict = venture_dict

        haurchefant = VentureButton(master, venture_dict, 'Haurchefant', bg='#0077EE')  # Teal
        josuke = VentureButton(master, venture_dict, 'Josuke', bg='#4400BB')  # Purple

        self.ventures = [josuke, haurchefant]
        self.mute_button = MuteButton(master, et).mute_button
        self.botanist_button = BotanistButton(master, et, FileDict('settings/settings'), outliner=Outliner())
        self.lock_image = ImageTk.PhotoImage(Image.open('icons/unlocked.png'))
        self.lock = Button(master,
                           image=self.lock_image,
                           bg='#000000',
                           borderwidth=0,
                           highlightcolor='#000000')

        WindowDraggaable(self.botanist_button.label, master)
        self.updates = [v.update for v in self.ventures] + [self.botanist_button.update]

        self.pack_buttons()
        # self.mute_button.pack_forget()

    def update_loop(self):
        for update in self.updates:
            update()

    def pack_buttons(self):
        kwargs = {'expand': True, 'fill': 'both'}

        # self.lock.pack(side='right', fill='both')
        for b in self.ventures:
            b.button.pack(side='right', fill='y')  # , **kwargs)

        self.mute_button.pack(side='right', fill='both', expand=True)  # , **kwargs)
        self.botanist_button.label.pack(side='right', **kwargs)

