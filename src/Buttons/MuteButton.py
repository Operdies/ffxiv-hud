from tkinter import Button, Label
from PIL import Image, ImageTk


class MuteButton:
    def __init__(self, master, et, mutefd):
        self.mutefd = mutefd
        self.et = et
        self.button = Button
        self.mute_icon = ImageTk.PhotoImage(Image.open('icons/mute.png'))
        self.unmute_icon = ImageTk.PhotoImage(Image.open('icons/unmute.png'))
        self.et.playing = self.mutefd['muted'] # it is toggled in mute_sound

        self.mute_button = Label(master,
                                 fg='#000000',
                                 bg='#000000',
                                 image=self.mute_icon if self.et.playing else self.unmute_icon,
                                 width=3,
                                 borderwidth=0,
                                 highlightthickness=0)

        self.mute_button.bind('<Button-1>', self.mute_sound)

    def mute_sound(self, e=None):
        self.et.playing = not self.et.playing
        self.mutefd['muted'] = self.et.playing
        self.mute_button.config(image=self.mute_icon if self.et.playing else self.unmute_icon)

