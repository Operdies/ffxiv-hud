from tkinter.ttk import Label, Button, Style
from PIL import Image, ImageTk


class MuteButton:
    def __init__(self, master, et, botanist_helper, settings):
        self.botanist_helper = botanist_helper
        self.settings = settings
        self.et = et
        self.button = Button
        style = Style()
        style.configure('mute.TLabel', width=-100, anchor='w')
        self.mute_icon = ImageTk.PhotoImage(Image.open('icons/mute.png'))
        self.unmute_icon = ImageTk.PhotoImage(Image.open('icons/unmute.png'))
        self.mute_button = Label(et.minimal_group,
                                 image=self.get_icon(),
                                 style='mute.TLabel')

        self.mute_button.bind('<Button-1>', self.mute_sound)

    def get_icon(self):
        return self.mute_icon if not self.settings['muted'] else self.unmute_icon

    def mute_sound(self, e=None):
        self.settings['muted'] = not self.settings['muted']
        self.mute_button.config(image=self.get_icon())
