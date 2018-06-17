from tkinter import Button, Label
from PIL import Image, ImageTk


class MuteButton:
    def __init__(self, master, et, botanist_helper, mutefd):
        self.botanist_helper = botanist_helper
        self.mutefd = mutefd
        self.et = et
        self.button = Button
        self.mute_icon = ImageTk.PhotoImage(Image.open('icons/mute.png'))
        self.unmute_icon = ImageTk.PhotoImage(Image.open('icons/unmute.png'))
        self.et.playing = self.mutefd['muted'] # it is toggled in mute_sound

        self.mute_button = Label(et.minimal_group,
                                 fg='#000000',
                                 bg='#000000',
                                 image=self.mute_icon if self.et.playing else self.unmute_icon,
                                 #width=3,
                                 height=28,
                                 borderwidth=0,
                                 highlightthickness=0)

        self.mute_button.bind('<Button-1>', self.mute_sound)

    def mute_sound(self, e=None):
        self.botanist_helper.playing = not self.botanist_helper.playing
        self.mutefd['muted'] = self.botanist_helper.playing
        self.mute_button.config(image=self.mute_icon if self.botanist_helper.playing else self.unmute_icon)

